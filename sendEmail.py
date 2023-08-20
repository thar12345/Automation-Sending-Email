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

isWorking = True

while (isWorking == True):
    value = int(input("Enter 1 to send an email, 2 to add to email list, 3 to delete from email list, 4 to view email list, 5 to quit: "))

    
    if (value == 1):
        subject = input("Enter subject of email: ")

        isSubjectWrong = True
        while (isSubjectWrong == True):  
            if (spell_check(subject)):    
                subject = input("Re-enter subject of email: ")
            else:
                isSubjectWrong = False 
        
        body = input("Enter body of email:")

        isBodyWrong = True
        while (isBodyWrong == True):  
            if (spell_check(body)):    
                body = input("Re-enter body of email: ")
            else:
                isBodyWrong = False  

        sender_email = "sendemailpython1@gmail.com"
        password = 'xfjhqysqcrtrgjbp'

        print("Sending Emails!")
        mycursor.execute("SELECT email FROM EmailRecords")
        receivers = mycursor.fetchall()
        for receiver in receivers:
            message = EmailMessage()
            message["From"] = sender_email
            message["To"] = receiver
            message["Subject"] = subject
            message.set_content(body)

            context = ssl.create_default_context() #gives us a context for a secure connection that we can use when using the smtp library and connecting to the Gmail Server

            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver, message.as_string())
        print("Success!")

    elif (value == 2):
        name = input("Enter the client's name: ")
        address = input("Enter the client's email address: ")

        mycursor.execute("INSERT INTO EmailRecords (name, email) VALUES(%s, %s)", (name, address))
        db.commit()
        print("Successfully Added!")

    elif (value == 3):
        address = input("Enter the client's email address: ")

        mycursor.execute("DELETE FROM EmailRecords WHERE email = %s", (address,))
        db.commit()
        print("Successfully Removed!")

    elif (value == 4):
        mycursor.execute("SELECT * FROM EmailRecords")
        result = mycursor.fetchall()
        for row in result:
            print(f"Name: {row[0]}, Email: {row[1]}")

    elif (value == 5):
        print("Have a nice day!")
        isWorking = False

    else:
        print("Invalid Option. Please try again.")

