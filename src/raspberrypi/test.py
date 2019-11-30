import datetime
import iwlist
import json
import os
# todo kalman filters https://www.wouterbulten.nl/blog/tech/kalman-filters-explained-removing-noise-from-rssi-signals/
scan_count = 500
print("scanning {} times...".format(scan_count))
data = []
empty_cell_data_count = 0
for i in range(scan_count):
    timestamp = datetime.datetime.now()
    content = iwlist.scan(interface='wlan0')  # takes 3 or 4 seconds
    cells = {"time": timestamp, "cells": iwlist.parse(content)}
    # save each scan to its own file, the filename being the timestamp
    if not os.path.exists("data"):
        os.mkdir("data")
    filename = "data/{:%Y%m%d_%H_%M_%S.%f}_scan{}.json".format(timestamp, i)
    with open(filename, 'wb') as fp:
        json.dump(cells, fp, sort_keys=True, indent=4, default=str)
        if cells is None or len(cells) < 1:
            empty_cell_data_count += 1
            print("scan {} failed, no cell data. saved data to {}".format(i, filename))
        else:
            print("scan {} complete. saved data to {}".format(i, filename))
print("scans with no data: {} of {}".format(empty_cell_data_count, scan_count))
