import subprocess

print("Hello world")

results = subprocess.check_output(["netsh", "wlan", "show", "network", "mode=Bssid"])
print(str(results).split("\\r\\n"))
# print(results)
