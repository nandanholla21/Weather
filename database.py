import sqlite3
import folium
path="C:/Users/Nandan Holla K/Documents/GitHub/Weather"
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
file.close()

name = input("Enter the name of the city you want to plot ")
if name=="":
    print("Enter valid city")
else:
    cur.execute('''
        SELECT * FROM Weather WHERE City = ?
    ''',(name,))
    row = cur.fetchone()
    if row is None:
        print("Record not found !")
    else:
        lat=row[2]
        long=row[3]
        m = folium.Map(location=[lat,long],zoom_start=7)
        folium.Marker(location=[lat,long],color="Red",popup=name).add_to(m)
        m.save(str(path)+"/map.html")
cur.close()