import json
import time

import requests
from bs4 import BeautifulSoup
import html_to_json
from ugg_sql import *


def login():
    s = requests.session()
    headers = {
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.ugg.com/ca/womens-slippers/tazz/1122553.html?dwvar_CHE_color=1122553',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
    }
    s.headers.update(headers)

    f = s.get('https://www.ugg.com/ca/login/')

    soup = BeautifulSoup(f.text, 'html.parser')
    all_class_topsection = soup.findAll('input', {'id': 'csrf_token'})

    output_json = html_to_json.convert(str(all_class_topsection))
    csrf = output_json['input'][0]['_attributes']['value']
    print(csrf)

    headers = {
        'content-length': '255',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://www.ugg.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.ugg.com/ca/login/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
    }

    s.cookies.update({
        "forterToken": "b51e2a6a9c0b406ca98c48d4e3375d6e_1701294095711__UDF43-m4_6"
    })

    payload = {
        "loginEmail": "joshuabeyer2@gmail.com",
        "loginPassword": "Jb021103@",
        "csrf_token": str(csrf)
    }

    s.post("https://www.ugg.com/on/demandware.store/Sites-UGG-CA-Site/en_CA/Account-Login", headers=headers,
           data=payload)
    return s


def spec(link):
    headers = {
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9'}
    payload = None

    response0 = requests.request("GET", link,
                                 headers=headers, data=payload)

    soup = BeautifulSoup(response0.text, 'html.parser')
    tracking_number = soup.findAll('span', {'class': 'summary-details'})
    orderInfo = {}


    orderInfo['date'] = (tracking_number[0]).text.strip("\n")

    try:

        if len(tracking_number) == 3:
            orderInfo['status'] = (tracking_number[2]).text.strip("\n")

        elif len(tracking_number) > 3:
            orderInfo['status'] = (tracking_number[3]).text.strip("\n")
            orderInfo['tracking'] = (tracking_number[4]).text.strip("\n")
    except:
        orderInfo['status'] = (tracking_number[2]).text.strip("\n")

    return orderInfo


def get_numbs(s, start):
    soup = (BeautifulSoup(s.get(
        "https://www.ugg.com/on/demandware.store/Sites-UGG-CA-Site/en_CA/Order-UpdateOrderHistory?start={}&sz=3".format(
            start)).text, 'html.parser'))

    order_numbers = soup.select('.card-header h4')
    orders = [x.text.strip().replace("Order No. ", "") for x in order_numbers]
    total_values = [total_span.text.strip() for total_span in
                    soup.select('div.dashboard-order-card-footer-columns span.dashboard-order-card-footer-value') if
                    "$" in total_span.text]
    href = [x.get('href') for x in soup.findAll('a', {'data-qa': 'orderDetails'})]

    final = {orders[x]: {"price": total_values[x], "link": href[x]} for x in range(len(order_numbers))}
    return final


def main():
    # s = login()
    # print(s.cookies.get_dict())
    # quit()
    # print(s.headers)
    s = requests.session()

    s.cookies.update({'forterToken': 'b51e2a6a9c0b406ca98c48d4e3375d6e_1701294095711__UDF43-m4_6', '__cq_dnt': '0', 'cqcid': 'acQsJZgqY7LMa5RfPWMV3GOJkv', 'cquid': '||', 'dw_dnt': '0', 'dwac_21efb91e77bdd04e3dc2603629': 'eSZ_3euh9Vm8WqvO0Q4VlaNAVcyv7TMLYI8%3D|dw-only|||CAD|false|US%2FPacific|true', 'dwanonymous_144c0595ba2614b5a686e169f60eb393': 'acQsJZgqY7LMa5RfPWMV3GOJkv', 'dwsid': 'JEQgFKSeEia6rp5HfU0coVkxBGbT4PMHNL0o6KJt03FQzpGSfpwocW1b312BRrcz0AAC4z0AONemAEymPEnMsw==', 'layer0_bucket': '40', 'layer0_destination': 'production', 'layer0_eid': 'd20030ea-c381-4652-94bd-53a3b1429d04', 'sid': 'eSZ_3euh9Vm8WqvO0Q4VlaNAVcyv7TMLYI8'})
    s.headers.update({
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'accept-encoding': 'gzip, deflate, br', 'accept': '*/*', 'Connection': 'keep-alive',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'x-requested-with': 'XMLHttpRequest', 'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"', 'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.ugg.com/ca/womens-slippers/tazz/1122553.html?dwvar_CHE_color=1122553',
        'accept-language': 'en-US,en;q=0.9'})

    # print(s.cookies.get_dict())
    # print(s.headers)

    ords = []
    start = 0

    while True:
        order_numbers = get_numbs(s, start)

        if not order_numbers:
            break

        # ords += order_number
        start += 3
        # print(ords)

        create_table()
        for i in order_numbers:
            add_order(i)
            update_order_info(i, price=order_numbers[i]['price'], link=order_numbers[i]['link'])

            print(get_order_info(i))

        time.sleep(4)


def get_new_orders():
    s = login()
    s.headers.update({
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'accept-encoding': 'gzip, deflate, br', 'accept': '*/*', 'Connection': 'keep-alive',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'x-requested-with': 'XMLHttpRequest', 'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"', 'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.ugg.com/ca/womens-slippers/tazz/1122553.html?dwvar_CHE_color=1122553',
        'accept-language': 'en-US,en;q=0.9'})
    start = 0

    all_ords = get_all_order_numbers()
    # print(all_ords)

    while True:
        order_numbers = get_numbs(s, start)
        # print(order_numbers)
        if not order_numbers:
            break

        # ords += order_number
        start += 3
        # print(ords)

        create_table()
        for i in order_numbers:
            if i in all_ords:
                return
            add_order(i)
            update_order_info(i, price=order_numbers[i]['price'], link=order_numbers[i]['link'])

            print(get_order_info(i))

        time.sleep(4)


def safe_save_all_info():
    count = 0
    for o in get_all_order_numbers():
        print(o)
        info = (get_order_info(o))
        if not info['delivery_status']:
            moreInfo = spec(info['link'])
            if 'tracking' in moreInfo:
                update_order_info(info['order_number'], delivery_status=moreInfo['status'], date=moreInfo['date'],
                                  tracking_number=moreInfo['tracking'])
            else:
                update_order_info(info['order_number'], delivery_status=moreInfo['status'], date=moreInfo['date'])

            count += 1



d = get_all_order_info()

sizes = {}

count = 0
while count <= 64:
    prod = (d[count].products)
    print(prod)
    if prod:
        prod = json.loads(prod)
        if prod[0]["item_name"] == "Tazz":
            if prod[0]['size'] not in sizes:
                sizes[prod[0]['size']] = int(prod[0]['quantity'])
            else:
                sizes[prod[0]['size']] += int(prod[0]['quantity'])
    count += 1

print(sizes)
quit()
# for i in d:
#     print(get_order_info(i))

safe_save_all_info()
quit()

quit()
# main()
# quit()

# Find all order numbers
create_table()
d = get_all_order_numbers()
for i in d:
    print(get_order_info(i))
quit()

# print(d)
