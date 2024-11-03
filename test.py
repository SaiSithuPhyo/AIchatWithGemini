import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
from pygame import mixer
from datetime import date

mixer.init()

# Set Google Gemini API key (replace with your actual key)
genai.configure(api_key="AIzaSyAnp-OK7Y2Vdb526wV21JqF3iNtWQSwN0M")

today = str(date.today())

# Name of Google Generative AI Model
model = genai.GenerativeModel('gemini-pro')

chat = model.start_chat()

# Text to speech function
def speak_text(text):
    mp3audio = BytesIO()
    tts = gTTS(text, lang='en-US', tld='us')
    tts.write_to_fp(mp3audio)
    mp3audio.seek(0)
    mixer.music.load(mp3audio, "mp3")
    mixer.music.play()
    while mixer.music.get_busy():
        pass
    mp3audio.close()

# Save conversation to a log file
def append2log(text):
    global today
    fname = 'chatlog-' + today + '.txt'
    with open(fname, "a", encoding='utf-8') as f:
        f.write(text + "\n")
        f.close

# Define default language
slang = "en-US"

# Main function
def main():
    global today

    rec = sr.Recognizer()
    mic = sr.Microphone()
    rec.dynamic_energy_threshold = False
    rec.energy_threshold = 400

    while True:
        with mic as source1:
            rec.adjust_for_ambient_noise(source1, duration=0.5)
            print("Listening...")
            audio = rec.listen(source1, timeout=20, phrase_time_limit=30)

            try:
                request = rec.recognize_google(audio, language=slang)
                if len(request) < 2:
                    continue

                # Send user input to Gemini model and receive response
                append2log(f"You: {request}\n")
                print(f"You: {request}\nAI: ")
                response = chat.send_message(request)
                print(response.text)
                speak_text(response.text.replace("*", ""))
                append2log(f"AI: {response.text}\n")

            except Exception as e:
                print(e)
                continue

if __name__ == "__main__":
    main()