import datetime
import time
import iwlist
import json

scan_count = 10
print("scanning {} times...".format(scan_count))
data = []
for i in range(scan_count):
    time.sleep(1)
    content = iwlist.scan(interface='wlan0')
    cells = {"time": datetime.datetime.now(), "cells": iwlist.parse(content)}
    data.append(cells)
    with open('data.json', 'wb') as fp:
        json.dump(data, fp, sort_keys=True, indent=4, default=str)
        print("scan {} complete. saved data to data.json".format(i))


