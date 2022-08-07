#!/usr/bin/python3
from __future__ import print_function
from ast import Sub
import  speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import pyjokes
import weather
import news
import googleAPI
import keyboard
import datetime
import csv
import serial
import serial.tools.list_ports

import os.path

listener = sr.Recognizer()

# for the serial communication with arduino my basic ports are 12 and 20
port ='COM20'
baud = 9600
arduino_ports = [
    p.device
    for p in serial.tools.list_ports.comports()
    if 'COM12' in p.description
]

# configuring google API for the sake of Calendar, Gmail, ...
    
if not arduino_ports:
    try:
        uno = serial.Serial(port, baud, timeout=1)
    except:
        print("[ERROR]: COULD NOT CONNECT WITH ARDUINO")
else:
    uno = serial.Serial(arduino_ports[0], baud, timeout=1)

def arduino(command):
    byte_msg = command.encode('utf-8')
    uno.write(byte_msg)
    

# voice engine starting
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    # function for text to speech
    engine.say(text)
    engine.runAndWait()

welcome = "[INFO]: what can I help"
talk(welcome)

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

def take_command_key():
    #This is to take commands from keyboard to make the testing easy
    command = input("[INPUT]: ")
    command = command.lower()
    return command

def run_friday(by):
    # This is series of if and else commands for different commands
    # handle the input keyboard or voice
    if by == 'key':
        command = take_command_key()
    elif by == 'voice':
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
    
    elif 'light' in command:
        # to tourn light off and on using arduino serial communication
        command = command.replace('light', '')
        if 'on' in command:
            # turn the light on
            response = "LIGHT IS ON"
            print("[INFO]: " + response)
            arduino('light_on')
            talk(response)
        elif 'off' in command:
            # turn the light off
            response = "LIGHT IS OFF"
            print("[INFO]: " + response)
            arduino('light_off')
            talk(response)

    elif 'room' in command:
        command = command.replace('room','')
        if 'info' in command:
            print("[INFO]: room Info")
            arduino('room_info')            
            response = uno.read(100).decode('utf-8').rstrip()
            print("[INFO]: "+ response)
            talk(response)
    
    elif 'my events' in command:
        events = googleAPI.ten_events()
        if not events:
            response = "No upcoming events"
            print("[INFO]: "+ response)
            talk(response)
        else:
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                response = (start, event['summary'])
                print("[INFO]: " + response)
                talk(response)

    elif 'read mail' in command:
        mails = googleAPI.gmail_main()
        if not mails:
            response = "No mails"
            print("[INFO]: "+response)
            talk(response)
        else:
            response = mails
            print(response)
            talk(response)

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
        print("[INPUT]: KEYBOARD")
        run_friday("key")
    elif keyboard.read_key() == "home":
        print("[INPUT]: VOICE")
        run_friday("voice")
    # And break the loop if [esc] button is touched
    elif keyboard.read_key() =="esc":
        print("[INFO] Existing")
        if uno:
            uno.close()
        break