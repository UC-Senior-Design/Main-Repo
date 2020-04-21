# How to config the pi for remote debugging

Just after formatting the sd card with the Raspbian OS, do the following:

make empty `ssh` file in `boot`.

make `wpa_supplicant.conf` file and include the following:

```conf
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="MULTI"
    psk="catdog12"
}
```

set the `ssid` to the ssid you want the pi to connect to. `psk` should be the password of that wifi network.

After inserting the sd card into the pi and booting the pi, the pi should connect to the network set in `wpa_supplicant.conf`.
The pi should be open to ssh because of the `ssh` file added to boot.

Connect to the pi over ssh. Setup static ip by typing in the following:

`sudo nano /etc/dhcpcd.conf`

Add these lines to `dhcpcd.conf`:

```conf
interface wlan0
static ip_address=192.168.X.Y/24
static routers=192.168.X.1
static domain_name_servers=192.168.X.1 8.8.8.8
```

make sure to set the ip addresses to the appropriate network you want the pi to connect to.

- X = the 3rd octet the access point is using.
- Y = Static IP you want the pi to use. Your pi will already have an ip address assigned by dhcp, you should use that as the static ip.

Save changes to `dhcpcd.conf` and restart the pi. it should boot up normally, connect to the network, and continue to use the static ip.