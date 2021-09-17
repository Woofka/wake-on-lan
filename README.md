# wake-on-lan
Simple script to send wake-on-lan packets

# Usage
```
usage: wake-on-lan.py [-h] [-d IPADDR] [-p PORT] MAC

positional arguments:
  MAC         MAC address of device to wake up

optional arguments:
  -h, --help  show this help message and exit
  -d IPADDR   IPv4 address of relay (default 255.255.255.255)
  -p PORT     Port to send the packet to (default 9)
```
