import os
import pytz
import time
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

load_dotenv()
client = OpenAI()

name = "Raj"

response = client.chat.completions.create(
  model="gpt-3.5-turbo-1106",
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

def schedule_message():
    try:
        message = client.messages.create(
                messaging_service_sid = os.getenv('TWILIO_MSG_SRVC_SID'),
                to = my_phone_num,
                body = f'{response.choices[0].message.content}',
                schedule_type = 'fixed',
                send_at = datetime(2023, 12, 15, 15, 14, 10)
            )
        print(message.sid)
    except TwilioRestException as e:
        print(e)
        raise

#print(time.tzname)
# print(response.choices[0].message.content)
schedule_message()
#message = client.messages.create(from_=twilio_phone_num, to=my_phone_num, body=f'{response.choices[0].message.content}')

