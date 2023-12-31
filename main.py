import os
import pytz
import time
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from fastapi import FastAPI

app = FastAPI()
load_dotenv()

client = OpenAI(
   api_key=os.environ.get("OPENAI_API_KEY"),
 )

name = "Raj"

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": f"Make me a short 1 sentence birthday wish for {name} as if you were a teenager, make it funny and cheery, use an emoji."}
  ]
)

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
my_phone_num = os.getenv("MY_PHONE_NUMBER")
twilio_phone_num = os.getenv("TWILIO_PHONE_NUMBER")
pacific_auck = pytz.timezone('Pacific/Auckland')
client = Client(account_sid, auth_token)

scheduled_time = datetime(2023, 12, 18, 22, 40, 10)
scheduled_time_utc = scheduled_time.astimezone(pytz.utc)

# TODO:
# Import SQL basemodel stuff, create friend data type to have name and phone number, pass that data type thru put and schedule_message
# If a phone number already exists, people can enter their name and phone number again, and a delete button will pop up and the add button 
# will be unclickable, so they can't add their bday again, and they'll receive an automated birthday message.

@app.put("/")
def schedule_message():
    try:
        message = client.messages.create(
                messaging_service_sid = os.getenv('TWILIO_MSG_SRVC_SID'),
                to = my_phone_num,
                body = f'{response.choices[0].message.content}',
                schedule_type = 'fixed',
                send_at = scheduled_time_utc
            )
        print(message.sid, f'{response.choices[0].message.content}')
    except TwilioRestException as e:
        print(e)
        raise
      
@app.delete("/{message_sid}")
def delete_message(message_sid:str):
  client.messages(message_sid) \
                .update(status='canceled')