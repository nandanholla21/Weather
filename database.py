from bs4 import BeautifulSoup
import json
from urllib.request import urlopen
import os
from dotenv import load_dotenv
import sqlite3
import folium
from flask import Flask, render_template, request , redirect
path="C:/Users/Nandan Holla K/Documents/GitHub/Weather"

app = Flask(__name__)
@app.route("/",methods=['GET'])
def home():
    s=[]
    conn = sqlite3.connect(str(path)+"/weatherdb.sqlite3")
    cur = conn.cursor()
    cur.execute('''DROP TABLE IF EXISTS Weather''')
    cur.execute(''' CREATE TABLE Weather(
        City Text,
        Temperature REAL,
        Latitude REAL,
        Longitude REAL,
        Country_Code Text
    );
    ''')

    filename = str(path)+"/database.txt"
    l=[]
    file = open(filename,"r")
    if not filename:
        print("File doesn't exist")
    else:
        for line in file:
            l=line.split(" ")
            city = l[0]
            temperature = round(float(l[1]),2)
            latitude = round(float(l[2]),4)
            longitude =round(float(l[3]),4)
            country_code = l[4]
            cur.execute('''
                SELECT * FROM Weather WHERE City = ?
            ''',(city,))
            row = cur.fetchone()
            if row is None:
                cur.execute('''
                INSERT INTO Weather(City,Temperature,Latitude,Longitude,Country_Code) VALUES (?,?,?,?,?)
                ''',(city,temperature,latitude,longitude,country_code,))
            else:
                cur.execute('''
                UPDATE Weather SET temperature =? WHERE City = ?
                ''',(temperature,city,))
        conn.commit()

    sqlstring="SELECT * FROM Weather"

    for row in cur.execute(sqlstring):
        print(row)
        s.append(row)
    file.close()
    return render_template("home.html",values=s)


@app.route("/weather-request",methods=['POST'])
def weather_req():
    if request.method == 'POST':
            path="C:/Users/Nandan Holla K/Documents/GitHub/Weather"
            conn = sqlite3.connect(str(path)+"/weatherdb.sqlite3")
            cur = conn.cursor()
            load_dotenv()
            API_KEY = os.getenv("API_KEY")

            file = open(str(path)+"/database.txt","a")
            city = request.form['input']
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
            cur.close()
    return redirect("/")

@app.route("/map-request",methods=['POST'])
def map_req():
    if request.method == 'POST':
        city = request.form['input']
        path="C:/Users/Nandan Holla K/Documents/GitHub/Weather"
        conn = sqlite3.connect(str(path)+"/weatherdb.sqlite3")
        cur = conn.cursor()
        cur.execute('''
            SELECT * FROM Weather WHERE City = ?
         ''',(city,))
        row = cur.fetchone()
        if row is None:
            print("Record not found !")
        else:
            lat=row[2]
            long=row[3]
            m = folium.Map(location=[lat,long],zoom_start=7)
            folium.Marker(location=[lat,long],color="Red",popup=city).add_to(m)
            m.save(str(path)+"/templates/map.html")
            return render_template("map.html")
        cur.close()
    return redirect("/")
if __name__ == '__main__':
    app.run(debug=True,port=3000)