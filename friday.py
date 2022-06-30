#!/usr/bin/python3
import  speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import weather
import news
import keyboard
import csv


listener = sr.Recognizer()

# voice engine starting
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    # function for text to speech
    engine.say(text)
    engine.runAndWait()

def take_command():
    # using the voice from the microphone
    # And this will change voice to text using speech_recognition library
    try:
        with sr.Microphone() as source:
            print("[+]: listening")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            # to make all given text lowercase
            command = command.lower()
            """if "friday" in command:
                command = command.replace('friday', '')
                print('[+]: command recived')"""
    except:
        # To handle every exceptions that could happen
        print("[+]: Exception handling")
        command = "error happens"
        pass
    return command


def run_friday():
    # This is series of if and else commands for different commands
    command = take_command()
    if 'play' in command:
        song = command.replace('play', '')
        print("playing" + song)
        talk('playing' + song)
        response = 'playing' + song
        # to play video on youtube
        pywhatkit.playonyt(song)
        
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print('Current time is ' + time)
        talk('Current time is ' + time)
        response = 'Current time is ' + time
        
    elif 'who is' in command or 'what is' in command:
        if 'who is' in command:
            person = command.replace('who is', '')
        elif 'what is' in command:
            person = command.replace('what is', '')
        try:
            info = wikipedia.summary(person, 1)
        except:
            info = "can not find {} in wikipedia".format(person)
        print(info)
        talk(info)
        response = info
        
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        print(joke)
        talk(joke)
        response = joke
        
    elif 'news' in command:
        command = command.replace('news', '')
        newss = news.News(command)
        for x in range(10):
            print(newss[x])
            talk(newss[x])
        response = newss
        
    elif 'weather' in command:
        # if weather is in the command
        x = weather.Weather()
        a = ("Temperature is " + x[0] + ", The Atmospheric pressure is " + x[1]
             + ", The Humidity is " + x[2] + ", weather condition is " + x[3] + ", With "
             + x[5] + "  wind speed at " + x[4] + ", with " + x[6] + " visibility and " + x[7] + " cloudiness")
        print("[INFO]" + a)
        talk(a)
        response = a

    elif 'error' in command:
        # if error happens speech_recognition
        info = "Error happens "
        print("[+]" + info)
        talk(info)
        response = info
    
    else:
        # if any of the above commads dones not work
        info = "please say the command again."
        print(info)
        talk(info)
        response = info
    
    # inorder to save every request and responses to csv file
    # for the of sake of MACHINE LEARNING
    data = [command, response, datetime.datetime.now()]
    with open('data.csv', 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)
    

while True:
    # It is only going to recive commands only if [insert] key are touched
    if keyboard.read_key() == "insert":
        print("[INFO] Key board pressed")
        run_friday()
    # And break the loop if [esc] button is touched
    elif keyboard.read_key() =="esc":
        print("[INFO] Existing")
        break
