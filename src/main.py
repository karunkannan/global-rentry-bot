import requests as req
import time
import os
from twilio.rest import Client

REQ_URL = "https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&locationId=%s&minimum=1&limit=1"
BOS_LOCATION_ID = 5441

SIGNUP_URL = "https://ttp.cbp.dhs.gov/"

TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH = os.environ['TWILIO_AUTH']

def send_sms(client: Client):
    if client == None:
        print("Error: twilio client is uninitialized")
    message = client.messages.create(body="Book global reentry: %s" % SIGNUP_URL, from_="+12568261687", to="+19784351861")

def check_appointments(client: Client) -> None:
    if client == None:
        print("Error: twilio client is uninitialized")
    appointments_response = req.get(REQ_URL % BOS_LOCATION_ID)
    if len(appointments_response.json()) > 0:
        send_sms(client)

def main() -> int:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH)
    while (True):
        check_appointments(client)
        time.sleep(20)
    return 0

if __name__=="__main__":
    main()
