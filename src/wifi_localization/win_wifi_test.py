from win_wifi import *

stuff = WinWiFi.scan()
thing = 1
for item in stuff:
    print("{}: {}".format(item.ssid, item.strength))
