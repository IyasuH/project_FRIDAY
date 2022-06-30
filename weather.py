#!/usr/bin/python3
# for handling weather request using openweathermap API key
import requests

api_key = "04681f65144b3fe5bad5940ff0493df7"  
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# default location
city_name = "Addis Ababa"
complete_url = base_url + "appid=" + api_key + "&q=" + city_name
response = requests.get(complete_url)
x = response.json()

def Weather():
    if x["cod"] != "404":
        # some of the information are to detail
        y = x["main"]
        cur_temp = str(round(y["temp"] - 273.15, 2)) + " °C"
        # max and min temp
        max_temp = str(round(y["temp_max"] - 273.15, 2)) + " °C"
        min_temp = str(round(y["temp_min"] - 273.15, 2)) + " °C"
        visibility = str(x["visibility"]) + " meter"# in m
        clouds =x["clouds"]
        clouds = str(clouds["all"]) + " %" # cloudiness %
        cur_pres = str(y["pressure"]) + " pascal"
        cur_humi = str(y["humidity"]) + " hygrometers"
        z = x["weather"]
        a = x["wind"]
        sys = x["sys"]
        # sunrise and set time
        sunrise = sys["sunrise"]
        sunset = sys["sunset"]
        wind_deg = str(a["deg"]) + " °"
        wind_speed = str(a["speed"]) + " meter per second"
        weather_desc = z[0]["description"]
            
        return(cur_temp, cur_pres, cur_humi, weather_desc, wind_deg, wind_speed, visibility, clouds)

    else:
        return(None)
        print(" City Not Found ")

