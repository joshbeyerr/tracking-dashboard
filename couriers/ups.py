import requests
import webbrowser
from adi_tracking.couriers.ups_sql import *
import time
import threading
import requests


token_lock = threading.Lock()


def accessToken():
    url = "https://wwwcie.ups.com/security/v1/oauth/token"

    payload = {
        "grant_type": "client_credentials"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "x-merchant-id": "string"
    }

    auth = 'L3VJg5LoUdGBpgPAK8opxQ2SdNOZWfni4aIudjeeAtLPeLqT', 'Gi7RYlLY2A0L997HLTCUeXWTJQMiGJtthnhHof9PswB0WHILKOLdULv8ufGSoWr3'

    response = requests.post(url, data=payload, headers=headers, auth=auth)

    data = response.json()
    return data


def refresh(ref_token):
    url = "https://onlinetools.ups.com/security/v1/oauth/refresh"

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": ref_token
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    auth = 'L3VJg5LoUdGBpgPAK8opxQ2SdNOZWfni4aIudjeeAtLPeLqT', 'Gi7RYlLY2A0L997HLTCUeXWTJQMiGJtthnhHof9PswB0WHILKOLdULv8ufGSoWr3'

    response = requests.post(url, data=payload, headers=headers, auth=auth)

    data = response.json()
    return data


def track(tracking, access_token):
    url = "https://onlinetools.ups.com/api/track/v1/details/" + tracking

    query = {
        "locale": "en_US",
        "returnSignature": "false"
    }

    headers = {
        "transId": "string",
        "transactionSrc": "testing",
        "Authorization": "Bearer {}".format(access_token)
    }
    response = requests.get(url, headers=headers, params=query)
    print(response.text)
    data = response.json()
    return data


def get_start_token():
    print("Getting New Tokens...")
    return accessToken()


def check_and_refresh_token():
    tokens = get_ups_tokens()
    if tokens:
        if (time.time() - (tokens['issued_at'] / 1000)) > 10000:
            with token_lock:
                # Check again to avoid race condition
                tokens = get_ups_tokens()
                if not tokens or (time.time() - (tokens['issued_at'] / 1000)) > 10000:
                    delete_ups_tokens()
                    create_table()
                    tokens = get_start_token()
                    print(tokens)
                    save_ups_tokens(tokens['access_token'], tokens['issued_at'])
    else:
        with token_lock:
            tokens = get_start_token()
            save_ups_tokens(tokens['access_token'], tokens['issued_at'])
    return tokens


def search(number, shipment):
    create_table()

    tokens = get_ups_tokens()

    try:
        s = (track(number, tokens['access_token']))['trackResponse']['shipment'][0]['package'][0]['activity']
    except:
        return False

    # print(s)
    ship = shipment()

    final = {x['status']['description']: x['date'] for x in s}

    ship.recentStatus = (list(final))[0]

    date = final[ship.recentStatus]

    if ", " in ship.recentStatus:
        ship.recentStatus = ship.recentStatus.split(', ')[0]

    ship.recentMonth = (date[4:6])
    ship.recentDay = int(date[6:])
    ship.set_recent()

    ship.tracking = number
    ship.history = final
    print(ship.history)

    if "delivered" in ship.recentStatus.lower():
        ship.delivered = True

    return ship
