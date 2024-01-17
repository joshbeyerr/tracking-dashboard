import requests
from flask import Flask, render_template, request, redirect, url_for
from track import allShipments, search, shipment, mass_search
from sites.ugg_sql import *
from sites.proper_ugg import spec
import threading
import json

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = Flask(__name__)

# Sample data structure to store tracking information
tracking_data_transit = []
tracking_data_delivered = []

shipmentsList = allShipments()

selected_ugg = []


@app.route('/')
def index(alert=None):
    shipmentsList.set_sorted()
    return render_template('index.html', tracking_data_delivered=shipmentsList.delivered,
                           tracking_data_transit=shipmentsList.transit, show_alert=alert)


def get_numbers():
    return [x.tracking for x in shipmentsList.allObj]


@app.route('/add', methods=['POST'])
def add_tracking():
    if request.method == 'POST':
        tracking_number = request.form['tracking_number']
        print(tracking_number)
        if ',' not in tracking_number:
            if tracking_number != "None":
                if tracking_number in get_numbers():
                    return index("Tracking Number Already Exists")

                try:
                    track_prod = search(tracking_number)
                    if not track_prod: return index("Tracking Not Available")
                except:
                    return index("Error With Tracking")

                track_prod.id = len(shipmentsList.allObj)
                track_prod.history = {key: value for key, value in reversed(track_prod.history.items())}
                shipmentsList.add_tracking(track_prod)

        else:
            track_list = list(set([x.strip(" ") for x in tracking_number.split(",")]))
            print(track_list)
            mass_search(shipmentsList, track_list)

        return redirect(url_for('index'))

    elif request.method == 'GET':
        return index("CANNOT GET")


@app.route('/delete/<item_id>', methods=['GET'])
def delete_tracking(item_id):
    shipmentsList.delete(item_id)
    return redirect(url_for('index'))


@app.route('/moreInfo/<item_id>', methods=['GET'])
def more_info(item_id):
    global tracking_data_transit

    focusData = {}
    for i in shipmentsList.allObj:
        if int(i.id) == int(item_id):
            focusData = i
            if focusData.history == {}:
                return index("Tracking Not Available")

    return render_template('info.html', tracking_data=focusData)


@app.route('/ugg', methods=['GET'])
def ugg(alert=None):
    all_orders = get_all_order_info()
    logger.info("here")

    return render_template('ugg.html',
                          ugg_orders=all_orders, show_alert=alert)


def ugg_reload_helper(order_num):
    moreInfo = spec(get_order_info(order_num))

    if 'tracking' in moreInfo:
        update_order_info(order_num, delivery_status=moreInfo['status'], date=moreInfo['date'],
                          tracking_number=moreInfo['tracking'])
        if "products" in moreInfo.keys():
            update_order_info(order_num, products=moreInfo['products'])

    else:
        update_order_info(order_num, delivery_status=moreInfo['status'], date=moreInfo['date'])
        if "products" in moreInfo.keys():
            update_order_info(order_num, products=moreInfo['products'])


@app.route('/reload', methods=['POST'])
def reload_ugg(alert=None):
    if request.method == 'POST':
        order_num = request.form['refresh']
        ugg_reload_helper(order_num)
        all_orders = get_all_order_info()

        return render_template('ugg.html',
                               ugg_orders=all_orders, show_alert=alert)

    elif request.method == 'GET':
        return index("CANNOT GET")


@app.route('/mass_ugg', methods=['POST'])
def mass_ugg(alert=None):
    ids = request.form.get('ids')
    try:
        ids = ids.split('-')
        start = int(ids[0])
        end = int(ids[1])
    except:
        return render_template('ugg.html',
                               ugg_orders=get_all_order_info(), show_alert="Invalid Id List")

    selected = []
    for x in get_all_order_info():
        if start <= x.id <= end:
            selected.append(x)
        elif x.id > end:
            break

    action = request.form.get('action')
    if action == 'mass_track':
        mass_search(shipmentsList, [x.tracking for x in selected if x.tracking is not None])
        return redirect(url_for('index'))

    elif action == 'display':
        prods = [item for x in selected if x.products for item in json.loads(x.products) if item['item_name']]


        print(prods)

        final = {}

        for g in prods:
            if g['item_name']:
                key = g['gender'] + g['color'] + g['item_name']
                if key not in final:
                    new = g
                    sizes = {int(new.pop('size')): int(new.pop('quantity'))}

                    new['sizes'] = sizes

                    final[key] = new
                else:
                    if int(g['size']) in final[key]['sizes']:
                        final[key]['sizes'][int(g['size'])] += int(g['quantity'])
                    else:
                        final[key]['sizes'][int(g['size'])] = int(g['quantity'])

        final = list(final.values())

        return render_template('products_display.html', products=final)
    else:

        threads = []
        for i in selected:
            thread = threading.Thread(target=ugg_reload_helper, args=([i.orderNumber]))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        return render_template('ugg.html',
                               ugg_orders=get_all_order_info(), show_alert=alert)


def get_tracking_info(tracking_number):
    # Implement your tracking API integration logic here
    # Replace this with actual tracking information retrieval logic
    return f"Tracking information for {tracking_number}"


if __name__ == '__main__':
    app.run(debug=True)
