# run locally, not on the pi
import matplotlib.pyplot as plt
import json
import os
import test
import statistics as statistics
import numpy as np

scan_file = "C:\\github\\SeniorDesign\\Main-Repo\\src\\WifiLocalization\\raspberrypi\\scan_data\\20191217_17_05_15.224575_scan-1.json"  # filename = ""
raw_distance_list = []
raw_24 = []
raw_5 = []
raw_24_rssi = []
raw_5_rssi = []
# data = []
with open(scan_file) as json_file:
    data = json.load(json_file)
    scan_count = 0
    for scan_group in data:
        if "cells" in scan_group:
            for scan in scan_group["cells"]:
                scan_distance = test.convert_rssi_to_meters(float(scan['signal_level_dBm']), float(scan['frequency']))
                scan['distance']['raw'] = scan_distance
                if scan_distance < 10:
                    raw_distance_list.append(scan_distance)
                    if float(scan['frequency']) > 4:
                        raw_5.append(scan_distance)
                        raw_5_rssi.append(float(scan['signal_level_dBm']))
                    else:
                        raw_24.append(scan_distance)
                        raw_24_rssi.append(float(scan['signal_level_dBm']))
                    # data.append(scan)
            scan_count += 1

print(
    f"2.4GHz\nmax: {max(raw_24_rssi)}\nmin: {min(raw_24_rssi)}\nrange: {max(raw_24_rssi) - min(raw_24_rssi)}\navg: {statistics.mean(raw_24_rssi)}")
print(
    f"5GHz\nmax: {max(raw_5_rssi)}\nmin: {min(raw_5_rssi)}\nrange: {max(raw_5_rssi) - min(raw_5_rssi)}\navg: {statistics.mean(raw_5_rssi)}")
# calculated distance histograms
n_bins = 10

# fig, axs = plt.subplots(1, 2, sharey=True)
# fig.suptitle("RSSI measurements at 1 meter distance")
# axs[0].hist(raw_24, bins=n_bins)
# axs[1].hist(raw_5, bins=n_bins)
# axs[0].set_title('2.4GHz')
# axs[1].set_title('5GHz')
# axs[0].set_xlabel('Distance (m)')
# axs[1].set_xlabel('Distance (m)')
# axs[0].set_ylabel('Measurement Count')

print(
    f"max: {max(raw_distance_list)}\nmin: {min(raw_distance_list)}\nrange: {max(raw_distance_list) - min(raw_distance_list)}")

# n, bins, patches = plt.hist(raw_distance_list, n_bins)
# plt.show()

# fucking stuff

# raw_distance_list = raw_distance_list[1500:]

def kalman(stuff):
    # initial parameters
    n_iter = len(stuff)
    sz = (n_iter,)  # size of array
    x = 1  # truth value
    z = stuff  # observations (normal about x, sigma=0.1)

    Q = 0.00001  # process variance. was 1e-5

    # allocate space for arrays
    xhat = np.zeros(sz)  # a posteri estimate of x
    P = np.zeros(sz)  # a posteri error estimate
    xhatminus = np.zeros(sz)  # a priori estimate of x
    Pminus = np.zeros(sz)  # a priori error estimate
    K = np.zeros(sz)  # gain or blending factor

    R = 0.1 ** 2  # estimate of measurement variance, change to see effect

    # initial guesses
    xhat[0] = 1.0
    P[0] = 1.0

    for k in range(1, n_iter):
        # time update
        xhatminus[k] = xhat[k - 1]
        Pminus[k] = P[k - 1] + Q

        # measurement update
        K[k] = Pminus[k] / (Pminus[k] + R)
        xhat[k] = xhatminus[k] + K[k] * (z[k] - xhatminus[k])
        P[k] = (1 - K[k]) * Pminus[k]
    return xhat

xhat_24 = kalman(raw_24)  # 2.4GHz
xhat_5 = kalman(raw_5)  # 5GHz

plt.figure()
plt.plot(raw_5, 'c.', label='5GHz unfiltered distance calculation')
plt.plot(xhat_5, 'b-', label='5GHz kalman estimate')
plt.plot(raw_24, 'm.', label='2.4GHz unfiltered distance calculation')
plt.plot(xhat_24, 'r-', label='2.4GHz kalman estimate')

plt.axhline(1, color='k', label='truth value')
plt.legend()
plt.title('Distance Estimate vs. Scan Iteration', fontweight='bold')
plt.xlabel('Scan Iteration')
plt.ylabel('Distance (m)')
plt.show()
