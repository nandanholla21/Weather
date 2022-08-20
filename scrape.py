from bs4 import BeautifulSoup
import json
from urllib.request import urlopen
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

path="C:/Users/Nandan Holla K/Documents/GitHub/Weather"

file = open(str(path)+"/database.txt","a")
print("Enter the city name you want to get the weather :")
city = input()
url= f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&mode=xml"

xml = urlopen(url)
soup = BeautifulSoup(xml,"xml")

#get the data
coord = soup("coord")
latitude = float(coord[0].attrs['lat'])
longitude = float(coord[0].attrs['lon'])
temperature = soup("temperature")
temp = round(float(temperature[0].attrs['value'])-273,2)  # to get temperature in celsius 

country_object = soup("country")
country = country_object[0].contents[0]

print(latitude)
print(longitude)
print(temp)
print(country)
# record = [city,temp,latitude,longitude,country]
file.write(str(city)+" "+str(temp)+" "+str(latitude)+" "+str(longitude)+" "+str(country)+"\n")
file.close()