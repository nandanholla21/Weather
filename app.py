from flask import Flask, render_template
from requests import request
import sqlite3
path="C:/Users/Nandan Holla K/Documents/GitHub/Weather"
conn = sqlite3.connect(str(path)+"/weatherdb.sqlite3")
cur = conn.cursor()
app = Flask(__name__)

@app.route('/')
def home():
    cur.execute("""SELECT * FROM Weather""")
    li = cur.fetchall()
    print(li)
    cur.close()
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True,port=3000)
