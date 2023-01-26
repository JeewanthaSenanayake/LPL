import mysql.connector
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
import time

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="lpl"
)


cred = credentials.Certificate(
    "D:\Pre_Eng\python\cricbuzz_scraper\lplrank-firebase-adminsdk-5651d-9acecc8c64.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


mycursor = mydb.cursor()

# select from table

mycursor.execute(
    "SELECT Pname,Batting,Bowling,All_Rounder FROM player_ranking")

myresult = mycursor.fetchall()

for x in myresult:
    print(x)
    data = {
        'batting': x[1],
        'bowlling': x[2],
        'allround': x[3],
    }

    name = x[0]
    db.collection('ratings').document(name).set(data)

updateDate = datetime.datetime.now()
time.mktime(updateDate.timetuple())
db.collection('updateTime').document('updateTime').set({'updateTime': time.mktime(updateDate.timetuple())})


