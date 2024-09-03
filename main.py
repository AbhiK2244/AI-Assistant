import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
newsApiKey = os.getenv("NEWS_APIKEY")
api = os.getenv("GIMINI_APIKEY")

recognizer = sr.Recognizer()
engine = pyttsx3.init()
genai.configure(api_key=api)

#assistant will say whatever text has been sent to this function
def speak(text):
    engine.say(text)
    engine.runAndWait()

#commands handler
def processCommand(c):
    #it will search on google chrome  -say "search for"
    if "search for" in c.lower():
        result = c.split("search for")
        webbrowser.open(f"https://google.com/search?q={result[1]}")

    # say "open google or youtube or instagram or linkedin or tweeter or youtube" to open these website.
    elif "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open tweeter" in c.lower():
        webbrowser.open("https://tweeter.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")

    # say "play songname (song should be present in the musicLibrary.py)" to play that song in youtube    
    elif "play" in c.lower():
        song = c.split("play ")[1]
        webbrowser.open(musicLibrary.music[song.lower()])
    # say "news" to get latest news of india    
    elif "news" in c.lower():          #tells the headlines of the news in india
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsApiKey}")
        if(r.status_code == 200):
            data = r.json()

            articles = data.get("articles", [])

            for article in articles:
                speak(article['title'])
                speak("the next news is")
    else:
        # if the requests are not handled by if and elifs then gimini will handle those requests
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"{c} and make sure give a short response and don't use any emoji or any images.")
        speak(response.text)

    print(c)

#main function
if __name__ == "__main__":
    speak("Initializing Jarvis")

    while True:
        # listen for the wake work "jarvis"
        recognizer = sr.Recognizer()

        try: 
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=1)

            print("recognising....")
            word = recognizer.recognize_google(audio)

            if(word.lower() == "jarvis"):
                speak("Ya")

                # now jarvis will listen for command
                with sr.Microphone() as source:
                    print("Jarvis Listening...")
                    audio = recognizer.listen(source)

                    command = recognizer.recognize_google(audio)
                    processCommand(command)
        except Exception as e:
            # speak("I didn't understand, what you said. ")
            print("error; {0}".format(e))