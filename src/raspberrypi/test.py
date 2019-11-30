import datetime
import math
import iwlist
import json
import os


# todo kalman filters
#  https://www.wouterbulten.nl/blog/tech/kalman-filters-explained-removing-noise-from-rssi-signals/


def convert_rssi_to_meters(rssi_dbm):
    """
    Converts RSSI (dBm) to meters
    Maths stolen from here: https://www.wouterbulten.nl/blog/tech/kalman-filters-explained-removing-noise-from-rssi-signals/
    >>> convert_rssi_to_meters(-22.5)
    1.0

    :param rssi_dbm: RSSI in dBm
    :return: distance in meters
    """
    d0 = 1.0  # 1 meter from AP used in A0
    A0 = -22.5  # referenced dBm value of AP at 1 meter distance
    n = 2.0  # signal propagation exponent (normally 2 for indoor environments)
    # model -> RSSI = -10 * n * log10(d/d0) + A0
    thing = (rssi_dbm - A0) / (-10.0 * n)
    return d0 * math.pow(10, thing)


def scan_and_get_data(mac_whitelist=[]):
    """
    Will scan all AP, filter out any that do not match the mac_whitelist,
    then return the data as a list of objects
    :param mac_whitelist: a list of mac addresses to white list the scan data
    :return: a list of scan data objects
    """
    _scan_timestamp = datetime.datetime.now()
    scan_content = iwlist.scan(interface='wlan0')  # takes 3 or 4 seconds
    _unfiltered_cells = iwlist.parse(scan_content)
    _filtered_cells = _unfiltered_cells
    if mac_whitelist is not None and len(mac_whitelist) > 0:
        _filtered_cells = [_i for _i in _unfiltered_cells if any(_sub in _i["mac"] for _sub in mac_whitelist)]
    _data = {"time": _scan_timestamp, "cells": _filtered_cells}
    return _data


# closest AP mac addresses
# 28:6D:9E:9E:D4 (2.412GHz)
# 28:6D:9E:9E:D0 (5.745GHz)
access_point_in_living_room = ["28:6D:9E:9E:D4", "28:6D:9E:9E:D0"]
print(convert_rssi_to_meters(-22.5))
scan_data = scan_and_get_data()
# quit()

scan_count = 500
print("scanning {} times...".format(scan_count))
all_data = []
empty_cell_data_count = 0
for i in range(scan_count):
    scan_data = scan_and_get_data(access_point_in_living_room)
    # save each scan to its own file, the filename being the timestamp
    if not os.path.exists("data"):
        os.mkdir("data")
    filename = "data/{:%Y%m%d_%H_%M_%S.%f}_scan{}.json".format(scan_data["time"], i)
    with open(filename, 'wb') as fp:
        if scan_data["cells"] is None or len(scan_data["cells"]) < 1:
            empty_cell_data_count += 1
            print("scan {} failed, no cell data. nothing saved to file.".format(i))
        else:
            all_data.append(scan_data)
            json.dump(scan_data, fp, sort_keys=True, indent=4, default=str)
            print("scan {} complete. saved data to {}".format(i, filename))
print("scans with no data: {} of {} total scans".format(empty_cell_data_count, scan_count))

