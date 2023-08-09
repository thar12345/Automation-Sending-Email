import mysql.connector
import smtplib
import ssl
from email.message import EmailMessage
import requests
import config

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Password1!",
)

mycursor = db.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS EmailRecords")
mycursor.execute("USE EmailRecords")
mycursor.execute("CREATE TABLE IF NOT EXISTS EmailRecords (name VARCHAR(255), email VARCHAR(255))")
