import requests as req
import time
from datetime import datetime, timedelta
import os
from twilio.rest import Client

REQ_URL = "https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&locationId=%s&minimum=1&limit=1"
BOS_LOCATION_ID = 5441

SIGNUP_URL = "https://ttp.cbp.dhs.gov/"

TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH = os.environ['TWILIO_AUTH']
PHONE_NUMBER = os.environ['PHONE_NUMBER']

last_sent_at = None

def send_sms(client: Client):
    if client == None:
        print("Error: twilio client is uninitialized")
    message = client.messages.create(body="Book global reentry: %s" % SIGNUP_URL, from_="+12568261687", to=PHONE_NUMBER)
    last_sent_at = datetime.now()
    

def check_appointments(client: Client) -> None:
    if client == None:
        print("Error: twilio client is uninitialized")
    appointments_response = req.get(REQ_URL % BOS_LOCATION_ID)
    send_message_cutoff = last_sent_at + timedelta(days=1)
    if len(appointments_response.json()) > 0 and datetime.now() > send_message_cutoff:
        send_sms(client)

def main() -> int:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH)
    while (True):
        check_appointments(client)
        time.sleep(2000)
    return 0

if __name__=="__main__":
    main()
