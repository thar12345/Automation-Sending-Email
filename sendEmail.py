import mysql.connector
import smtplib
import ssl
from email.message import EmailMessage
import requests
import config

def spell_check(text):
    url = "https://grammarbot.p.rapidapi.com/check"

    payload = {
        "text": text,
        "language": "en-US"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": config.key,
        "X-RapidAPI-Host": "grammarbot.p.rapidapi.com"
    }

    response = requests.post(url, data=payload, headers=headers)

    
    try:
        print(response.json()['matches'][0]['message'])
        return True
    except:
        return False



db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Password1!",
)

mycursor = db.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS EmailRecords")
mycursor.execute("USE EmailRecords")
mycursor.execute("CREATE TABLE IF NOT EXISTS EmailRecords (name VARCHAR(255), email VARCHAR(255))")
