import requests
from bs4 import BeautifulSoup
import html_to_json


def get_data(egData):
    dataMain = (egData['div'][0]['div'][0]['div'][1]['div'][0]['div'][1]['div'][0]['div'])
    history = {}

    for x in dataMain:
        if x["_attributes"]['class'] == ['row', 'listable']:
            history[x['div'][0]['span'][1]['_value']] = x['div'][1]['span'][0]['_value']

    return history


# format of [month, day, time]
def format_time(data):
    month_dict = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12"
    }
    daySplit = data[0].split(" ")
    return [month_dict[daySplit[0]], daySplit[1], data[1]]


def search(tracking_number, shipment):
    s = requests.session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Referer": "https://direct.tfesg.com/finalmiletrack/Track"
    })

    data = {"trackingNumber": tracking_number}
    track = s.post('https://direct.tfesg.com/finalmiletrack/Track', data=data)
    soup = BeautifulSoup(track.text, 'html.parser')
    history = get_data(html_to_json.convert(str((soup.findAll('div', {'class': 'col-xs-12'}))[3])))

    prod = shipment()
    prod.tracking = tracking_number
    prod.history = history

    prod.recentStatus = list(history)[0]

    recent = format_time((history[list(history)[0]]).split(" - "))
    prod.recentMonth = recent[0]
    prod.recentDay = recent[1]
    prod.recentTime = recent[2]

    prod.set_recent()

    if "Delivered" in prod.recentStatus:
        prod.delivered = True

    return prod

