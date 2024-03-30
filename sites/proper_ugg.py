import requests
from bs4 import BeautifulSoup
import json
# for use in app


def spec(order):
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

    response0 = requests.request("GET", order.link,
                                 headers=headers, data=payload)

    soup = BeautifulSoup(response0.text, 'html.parser')
    tracking_number = soup.findAll('span', {'class': 'summary-details'})

    orderInfo = {'date': (tracking_number[0]).text.strip("\n")}

    if not order.products:
        quan = soup.findAll('span', {'class': 'pricing qty-card-quantity-count'})

        product_details = soup.findAll('div', {'class': 'product-line-item-details d-flex flex-row'})

        def extract_product_info(element):
            # print(element)
            try:
                product_info = {'item_name': element.find('img', class_='product-image')['alt'],
                                'image_link': element.find('img', class_='product-image')['src']}

            except:
                product_info = {'item_name': None,
                                'image_link': None}

            attributes = element.find_all('p', class_='line-item-attributes')
            product_info['gender'] = attributes[0].get_text()
            product_info['color'] = attributes[1].get_text().split(': ')[1]
            product_info['size'] = attributes[2].get_text().split(': ')[1]

            return product_info

        extracted_info = []
        count = 0
        for html in product_details:
            product_info = extract_product_info(html)
            product_info['quantity'] = quan[count].text.strip("\n")
            extracted_info.append(product_info)
            count += 1
        print(extracted_info)
        order.products = extracted_info

        orderInfo['products'] = json.dumps(extracted_info)

    tracking_number.pop(0)
    tracking_number.pop(0)

    for i in tracking_number:
        i = i.text.strip("\n")
        if '1Z' in i:
            orderInfo['tracking'] = i
        else:
            orderInfo['status'] = i

    return orderInfo

