from win_wifi import *

stuff = WinWiFi.scan()
thing = 1
for item in stuff:
    print(item.ssid)
    count = 1
    for bssid in item.bssids.keys():
        print("  {} - {} - {} - {}".format(count, bssid, item.bssids[bssid], ((item.bssids[bssid] / 2) - 100)))
        count += 1
    # print("{}: {}".format(item.ssid, item.strength))


