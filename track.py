from adi_tracking.couriers import ups, tforce, purolator
import threading


class allShipments:
    def __init__(self):
        self.allObj = []

        self.transit = set()
        self.delivered = set()

    def add_tracking(self, obj):
        self.allObj.append(obj)
        self.set_sorted()

    def set_sorted(self):
        self.transit = (x for x in self.allObj if x.delivered == False)
        self.delivered = (x for x in self.allObj if x.delivered)

    def delete(self, id):
        self.allObj = [x for x in self.allObj if int(x.id) != int(id)]
        for i in range(len(self.allObj)):
            self.allObj[i].id = i

        self.set_sorted()


class shipment:
    def __init__(self):
        self.tracking = None
        self.courier = None
        self.history = None
        self.recent = None
        self.recentMonth = None
        self.recentDay = None
        self.recentTime = None
        self.recentStatus = None
        self.id = None
        self.delivered = False
        self.estimated = None
        self.order = None

    def all_tracking(self, tracking_list):
        return [x.tracking for x in tracking_list]

    def set_recent(self):
        month_dict = {
            "01": 'Jan',
            "02": 'Feb',
            "03": 'Mar',
            "04": 'Apr',
            "05": "May",
            "06": "Jun",
            "07": "Jul",
            "08": "Aug",
            "09": "Sep",
            "10": "Oct",
            "11": "Nov",
            "12": "Dec"
        }
        self.recent = "{}: {} {} {}".format(self.recentStatus, month_dict[self.recentMonth], self.recentDay, self.recentTime if self.recentTime else "")


def search(num):
    if ("{}{}".format(num[0], num[1])).lower() == "1z":
        ups.check_and_refresh_token()
        return ups.search(num, shipment)
    elif ("{}{}".format(num[0], num[1])).lower() == "aw":
        print('here')
        return purolator.main(num, shipment)

    else:
        return tforce.search(num, shipment)


def mass_search(shipList, track_list):
    def mass_tracking(tracking_number):
        print(tracking_number)
        if tracking_number != "None":
            if tracking_number in [x.tracking for x in shipList.allObj]:
                return
            try:
                track_prod = search(tracking_number)
                if not track_prod: return
            except:
                return

            track_prod.id = len(shipList.allObj)
            track_prod.history = {key: value for key, value in reversed(track_prod.history.items())}
            shipList.add_tracking(track_prod)
            return
    threads = []

    ups.check_and_refresh_token()

    print(track_list)
    for i in range(len(track_list)):
        thread = threading.Thread(target=mass_tracking, args=([track_list[i]]))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("done threads")

