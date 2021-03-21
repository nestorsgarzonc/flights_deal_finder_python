from models.flight_deals import FlightDeals
import dotenv
import os
import requests
from pprint import pprint
import json

dotenv.load_dotenv()

SHEETY_ENDPOINT = os.getenv('SHEETY_ENDPOINT')
SHEETY_TOKEN = os.getenv('SHEETY_TOKEN')
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
TWILIO_PHONE = os.getenv('TWILIO_PHONE')
KIWI_TOKEN = os.getenv('KIWI_TOKEN')

sheety_headers = {'Authorization': SHEETY_TOKEN}


def get_sheety_data():
    res = requests.get(
        SHEETY_ENDPOINT,
        headers=sheety_headers,
    )
    res = res.json()['prices']

    data = [FlightDeals(city=i['city'], iataCode=i['iataCode'],
                        id=i['id'], lowestPrice=i['lowestPrice'], ) for i in res]
    return data


sheety_data = get_sheety_data()
for e in sheety_data:
    element_json = e.to_json()
    endpoint = f'{SHEETY_ENDPOINT}/{e.id}'
    res = requests.put(
        endpoint,
        json={'price': element_json},
        headers={**sheety_headers, 'Content-Type': 'application/json'},
    )
    print(res.json())
    print(res.status_code)
