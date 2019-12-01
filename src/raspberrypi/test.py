import datetime
import math
import iwlist
import json
import os
import sys


# This file will scan wifi RSSI values and save each scan to a json file

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


def parse_with_distance(scan_content):
    """
    Given raw scan content from iwlist.parse(), will parse it into a known object with distance calculations
    :param scan_content: raw scan content
    :return: formatted scan data
    """
    parsed_cells = iwlist.parse(scan_content)
    for cell in parsed_cells:
        cell["distance"] = {"raw": convert_rssi_to_meters(float(cell["signal_level_dBm"])), "kalman": 0.0}  # todo kalman
    return parsed_cells


def scan_and_get_data(mac_whitelist=[]):
    """
    Will scan all AP, filter out any that do not match the mac_whitelist,
    then return the data as a list of objects
    :param mac_whitelist: a list of mac addresses to white list the scan data
    :return: a list of scan data objects
    """
    _scan_timestamp = datetime.datetime.now()
    scan_content = iwlist.scan(interface='wlan0')  # takes 3 or 4 seconds
    _unfiltered_cells = parse_with_distance(scan_content)
    _filtered_cells = _unfiltered_cells
    if mac_whitelist is not None and len(mac_whitelist) > 0:
        _filtered_cells = [_i for _i in _unfiltered_cells if any(_sub in _i["mac"] for _sub in mac_whitelist)]
    _data = {"time": _scan_timestamp, "cells": _filtered_cells}
    return _data


def save_data_to_file(_scan_data, _filename, scan_index):
    """
    Save scan data to file
    :param _scan_data: scan data
    :param _filename: name and dir of file to save to
    :param scan_index: scan index of all scans in the scan loop
    :return: None
    """
    with open(_filename, 'w') as fp:
        json.dump(_scan_data, fp, sort_keys=True, indent=4, default=str)
        print(f"scan {scan_index} complete. saved data to {_filename}")


def setup_storage():
    """
    Sets up storage directory for all saved scan data
    :return: scan directory
    """
    scan_dir = "/home/pi/scan_data"
    if not os.path.exists(scan_dir):
        os.mkdir(scan_dir)
    return scan_dir


def get_filename(scan_time, scan_index):
    """
    Returns the filename for a given scan
    :param scan_time: time of scan
    :param scan_index: scan index of all scans in the scan loop
    :return: name of file for input scan
    """
    return f"{scan_time:%Y%m%d_%H_%M_%S.%f}_scan{scan_index}.json"


def get_save_file_path(scan_time, scan_index):
    return f"{setup_storage()}/{get_filename(scan_time, scan_index)}"


def start_scan_loop(scan_count=50):
    """
    Scans and saves data of each scan to json file.
    :param scan_count: number of times to scan
    :return: None
    """
    # closest AP mac addresses
    # 28:6D:9E:9E:D4 (2.412GHz)
    # 28:6D:9E:9E:D0 (5.745GHz)
    access_point_in_living_room = ["28:6D:9E:9E:D4", "28:6D:9E:9E:D0"]
    print(f"scanning {scan_count} times...")
    all_data = []
    empty_cell_data_count = 0
    for i in range(scan_count):
        scan_data = scan_and_get_data(access_point_in_living_room)
        if scan_data["cells"] is None or len(scan_data["cells"]) < 1:
            empty_cell_data_count += 1
            i -= 1  # restart scan, don't know if this is the best idea, but it seems to work just fine
            print(f"scan {i} failed, no cell data. nothing saved to file.")
        else:
            save_data_to_file(scan_data, get_save_file_path(scan_data["time"], i), i)
            all_data.append(scan_data)
    if empty_cell_data_count > 0:
        print(f"scans with no data: {empty_cell_data_count} of {scan_count} total scans")
    else:
        print(f"all {scan_count} scans successful")


if __name__ == '__main__':
    scan_count = 100
    if len(sys.argv) > 1:
        scan_count = sys.argv[1]
    start_scan_loop(int(scan_count))
