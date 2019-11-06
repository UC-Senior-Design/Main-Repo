from win_wifi import *

stuff = WinWiFi.scan()
thing = 1
for item in stuff:
    print(item.ssid)
    for bssid in item.bssids.keys():
        print("{} - {}".format(bssid, item.bssids[bssid]))
    # print("{}: {}".format(item.ssid, item.strength))


