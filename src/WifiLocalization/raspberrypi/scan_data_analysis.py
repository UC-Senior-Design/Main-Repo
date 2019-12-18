# run locally, not on the pi
import matplotlib.pyplot as plt
import json
import os
import test

scan_file = "C:\\github\\SeniorDesign\\Main-Repo\\src\\WifiLocalization\\raspberrypi\\scan_data\\20191217_17_05_15.224575_scan-1.json"# filename = ""
raw = []
data = []
with open(scan_file) as json_file:
    data = json.load(json_file)
    scan_count = 0
    for scan_group in data:
        if "cells" in scan_group:
            for scan in scan_group["cells"]:
                scan_distance = test.convert_rssi_to_meters(float(scan['signal_level_dBm']), float(scan['frequency']))
                scan['distance']['raw'] = scan_distance
                if scan_distance < 10:
                    # print(f"scan raw: {scan['distance']['raw']}")
                    raw.append(scan_distance)
                    data.append(scan)
            scan_count += 1

# for filename in os.listdir(directory):
#     with open(directory + "\\" + filename) as json_file:
#         data = json.load(json_file)
#         for scan in data["cells"]:
#             if float(scan["frequency"]) < 5 and scan['distance']['raw'] < 10:
#                 # print(f"scan raw: {scan['distance']['raw']}")
#                 raw.append(scan['distance']['raw'])

print(f"max: {max(raw)}\nmin: {min(raw)}\nrange: {max(raw) - min(raw)}")
n_bins = 10
n, bins, patches = plt.hist(raw, n_bins)
plt.show()

# redo 5GHz scan data
# test.save_data_to_file(data, scan_file)
