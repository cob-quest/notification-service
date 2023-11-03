import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SMTP_API_KEY")

url = "https://api.smtp2go.com/v3/email/send"
headers = {"Content-Type": "application/json"}

with open("file.csv","r") as csv_file:
    next(csv_file)
    for row in csv_file:
        txt = row.split(",")
        user = txt[0]
        password = txt[1]
        secret_key = txt[2]
        access_key = txt[3]

        message = f"Hello {user}, your password is {password}, secret key is {secret_key}, access key is {access_key}"
        # print(message)
        receiver_arr = ["Test Person <ojh809@gmail.com>"]
        data = {}
        data["api_key"] = api_key
        data["to"] = receiver_arr
        data["sender"] = "Test Persons Friend <gabriel.ong.2021@scis.smu.edu.sg>"
        data["subject"] = "Hello World"
        data["text_body"] = message
        
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            print("Email sent successfully!")
            print(response.json())
        else:
            print("Failed to send the email.")
            print(response.text)