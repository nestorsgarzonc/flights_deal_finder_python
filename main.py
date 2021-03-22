from models.flight_deals import FlightDeals
import dotenv
import os
import requests

dotenv.load_dotenv()

SHEETY_ENDPOINT = os.getenv('SHEETY_ENDPOINT')
SHEETY_TOKEN = os.getenv('SHEETY_TOKEN')
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
TWILIO_PHONE = os.getenv('TWILIO_PHONE')
KIWI_TOKEN = os.getenv('KIWI_TOKEN')
KIWI_ENDPOINT = 'https://tequila-api.kiwi.com'
sheety_headers = {'Authorization': SHEETY_TOKEN}


def get_sheety_data():
    res = requests.get(SHEETY_ENDPOINT, headers=sheety_headers,)
    res = res.json()['prices']
    data = [FlightDeals(city=i['city'], iataCode=i['iataCode'],
                        id=i['id'], lowestPrice=i['lowestPrice'], ) for i in res]
    return data


def get_iata_data(data: FlightDeals):
    endpoint = f'{KIWI_ENDPOINT}/locations/query'
    res = requests.get(
        endpoint,
        headers={'apikey': KIWI_TOKEN},
        params={'location_types': 'city', 'term': data.city}
    )
    return res.json()['locations'][0]['code']


sheety_data = get_sheety_data()


def update_iata():
    for e in sheety_data:
        iata = get_iata_data(e)
        e.iataCode = iata
        element_json = e.to_json()
        endpoint = f'{SHEETY_ENDPOINT}/{e.id}'
        requests.put(
            endpoint,
            json={'price': element_json},
            headers={**sheety_headers, 'Content-Type': 'application/json'},
        )
    print(sheety_data)


update_iata()
