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
    A0 = -22.5  # referenced dBm value of AP at 1 meter distance, this will be different if the client and AP are different than my original scan
    n = 2.0  # signal propagation exponent (normally 2 for indoor environments)
    # model -> RSSI = -10 * n * log10(d/d0) + A0
    thing = (rssi_dbm - A0) / (-10.0 * n)
    return d0 * math.pow(10, thing)


def parse_and_format(scan_content, scan_timestamp):
    """
    Given raw scan content from iwlist.parse(), will parse it into a known object with distance calculations
    :param scan_timestamp: time of scan
    :param scan_content: raw scan content
    :return: formatted scan data
    """
    parsed_cells = iwlist.parse(scan_content)
    for cell in parsed_cells:
        cell["distance"] = {"raw": convert_rssi_to_meters(float(cell["signal_level_dBm"])), "kalman": -1.0}  # todo kalman
        cell["time"] = scan_timestamp
    return parsed_cells


def filter_mac(unfiltered_cells, mac_whitelist=[]):
    filtered_cells = unfiltered_cells
    if mac_whitelist is not None and len(mac_whitelist) > 0:
        filtered_cells = [_i for _i in unfiltered_cells if any(_sub in _i["mac"] for _sub in mac_whitelist)]
    return filtered_cells


def scan_and_get_data(mac_whitelist=[]):
    """
    Will scan all AP, filter out any that do not match the mac_whitelist,
    then return the data as a list of objects
    :param mac_whitelist: a list of mac addresses to white list the scan data
    :return: a list of scan data objects
    """
    scan_timestamp = datetime.datetime.now()
    scan_content = iwlist.scan(interface='wlan0')  # takes 3 or 4 seconds
    unfiltered_cells = parse_and_format(scan_content, scan_timestamp)
    filtered_cells = filter_mac(unfiltered_cells, mac_whitelist)
    formatted_scan_data = {"time": scan_timestamp, "cells": filtered_cells}
    return formatted_scan_data


def save_data_to_file(scan_data, filename):
    """
    Save scan data to file
    :param scan_data: scan data
    :param filename: name and dir of file to save to
    :return: None
    """
    with open(filename, 'w') as fp:
        json.dump(scan_data, fp, sort_keys=True, indent=4, default=str)
    return filename


def setup_storage():
    """
    Sets up storage directory for all saved scan data
    :return: scan directory
    """
    scan_dir = "/home/pi/scan_data"  # this can be changed if the data should be saved in a different dir
    if not os.path.exists(scan_dir):
        os.mkdir(scan_dir)
    return scan_dir


def get_filename(scan_time, scan_index=-1):
    """
    Returns the filename for a given scan
    :param scan_time: time of scan
    :param scan_index: scan index of all scans in the scan loop
    :return: name of file for input scan
    """
    return f"{scan_time:%Y%m%d_%H_%M_%S.%f}_scan{scan_index}.json"


def get_save_file_path(scan_time, scan_index=-1):
    return f"{setup_storage()}/{get_filename(scan_time, scan_index)}"


def increment_scan_count(scan_count, i):
    """
    Used to always keep scan_count equal to or greater than 0
    :param scan_count: current count of scans
    :param i: number to increment by
    :return: scan_count >= 0
    """
    if i < 0 and scan_count <= 0:
        return 0
    else:
        return scan_count + i


def start_scan_loop(total_scans, mac_whitelist):
    """
    Scans and saves data of each scan to json file.
    :param mac_whitelist: a list of mac addresses to white list the scan data
    :param total_scans: number of times to scan
    :return: None
    """
    print(f"scanning {total_scans} times...")
    all_data = []
    empty_cell_data_count = 0
    scan_count = 0
    while scan_count <= total_scans:
        scan_data = scan_and_get_data(mac_whitelist)
        if scan_data["cells"] is None or len(scan_data["cells"]) < 1:
            empty_cell_data_count += 1
            scan_count = increment_scan_count(scan_count, -1)  # restart this scan
            print(f"scan {scan_count} failed, no cell data. nothing saved to file.")
        else:
            filename = save_data_to_file(scan_data, get_save_file_path(scan_data["time"], scan_count))
            print(f"scan {scan_count} complete. saved data to {filename}")
            all_data.append(scan_data)
            scan_count = increment_scan_count(scan_count, 1)  # continue to next scan
    print("Scanning complete.")
    all_data_filename = save_data_to_file(all_data, get_save_file_path(datetime.datetime.now()))
    print(f"all scan data saved to file: {all_data_filename}")
    if empty_cell_data_count > 0:
        print(f"DONE | Number scans with no data: {empty_cell_data_count} of {total_scans} total scans")
    else:
        print(f"DONE | all {total_scans} scans successful")


if __name__ == '__main__':
    # closest AP mac addresses
    # 28:6D:9E:9E:D4 (2.412GHz)
    # 28:6D:9E:9E:D0 (5.745GHz)
    access_point_in_living_room = ["28:6D:9E:9E:D4", "28:6D:9E:9E:D0"]
    total_number_of_scans = 100
    if len(sys.argv) > 1:
        total_number_of_scans = int(sys.argv[1])
    start_scan_loop(total_number_of_scans, access_point_in_living_room)
