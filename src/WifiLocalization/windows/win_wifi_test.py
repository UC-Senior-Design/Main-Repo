from win_wifi import *
from statistics import mean
import datetime


def convert_percent_to_db(percent):
    return (percent / 2) - 100


def get_bssid_avg(_scans: dict, _bssid: str):
    bssid_signals: list = []
    bssid_count = 0
    for scan in _scans.values():
        for ssid in scan:
            if _bssid in ssid.bssids:
                bssid_signals.append(ssid.bssids[_bssid])
                bssid_count += 1
    return mean(bssid_signals)


def get_bssid_range(_scans: dict, _bssid: str):
    bssid_signals: list = []
    bssid_count = 0
    for scan in _scans.values():
        for ssid in scan:
            if _bssid in ssid.bssids:
                bssid_signals.append(ssid.bssids[_bssid])
                bssid_count += 1
    return max(bssid_signals) - min(bssid_signals)


scans: int = 20
print("Initializing {} scan(s). Do not move WiFi antenna.\n".format(scans))
scan_timeline: dict = {}
for i in range(0, scans):
    scan_timeline[datetime.datetime.now()] = WinWiFi.scan()
    print("scan {} of {} complete.".format(i + 1, scans))
    time.sleep(1)

# range, avg, what else

for scan in scan_timeline.values():
    for ssid in scan:
        for bssid in ssid.bssids:
            print("{:30} - {} - avg {:6.2f} - range {:3}".format(ssid.ssid, bssid, get_bssid_avg(scan_timeline, bssid), get_bssid_range(scan_timeline, bssid)))
    break

# avg = {}
# _range = {}
# ssid_count = 1
# for i in range(0, scans):
#     for ssid_scan_data in stuff[i]:
#         print("{} - {}".format(ssid_count, ssid_scan_data.ssid))
#         bssid_count = 1
#
#         for bssid in ssid_scan_data.bssids.keys():
#             print("  {} - {} - {} - {}".format(bssid_count, bssid, ssid_scan_data.bssids[bssid],
#                                                convert_percent_to_db(ssid_scan_data.bssids[bssid])))
#             bssid_count += 1
#         ssid_count += 1

# for item in stuff:
#     print("{} - {}".format(ssid_count, item.ssid))
#     bssid_count = 1
#     for bssid in item.bssids.keys():
#         print("  {} - {} - {} - {}".format(bssid_count, bssid, item.bssids[bssid], convert_percent_to_db(item.bssids[bssid])))
#         bssid_count += 1
#     ssid_count += 1
    # print("{}: {}".format(item.ssid, item.strength))


