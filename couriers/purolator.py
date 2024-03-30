import requests
import os
from dotenv import load_dotenv


def main(tracking, shipment):
    load_dotenv()

    s = requests.session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'X-Api-Key': os.environ.get('PUROLATORKEY')
    })
    data = {"search": [{"trackingId": "{}".format(tracking), "sequenceId": 1, "eventSortOrder": "d"}], "language": "en"}
    try:
        response = next((pkg for pkg in
                         (s.post("https://track.purolator.com/tracking-ext/v1/search", json=data)).json()['shipment'][
                             0]['package'] if pkg['pin'].upper() == tracking.upper()), None)
        print(response)
    except:
        return

    ship = shipment()
    ship.tracking = tracking
    ship.courier = "Purolator"
    final = {x['description']: x['dateTime'] for x in response['events']}

    ship.history = final

    ship.recentStatus = response['lastEvent']['description']
    if ship.recentStatus == 'Shipment delivered':
        ship.delivered = True
    date = (response['lastEvent']['dateTime'].split(" "))[0].split('-')

    ship.recentMonth = date[1]
    ship.recentDay = date[2]
    ship.set_recent()
    ship.estimated = response['estimatedDeliveryDate']
    return ship
