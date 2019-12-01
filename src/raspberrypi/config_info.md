# How to config the pi for remote debugging

make ssh file

make wpa_supplicant.conf file

```conf
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="MULTI"
    psk="catdog12"
}
```

setup static ip

`sudo nano /etc/dhcpcd.conf`

add these lines:

```conf
interface eth0
static ip_address=192.168.137.187/24
static routers=192.168.137.1
static domain_name_servers=192.168.137.1 8.8.8.8
interface wlan0
static ip_address=192.168.137.188/24
static routers=192.168.137.1
static domain_name_servers=192.168.137.1 8.8.8.8
```
