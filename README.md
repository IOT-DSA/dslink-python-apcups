# dslink-python-apcups
This is a DSLink that communicates with APC(and similar UPSes) to retrieve information from the power supply itself, over USB.

## Setup
### Linux
To install the system service and utilities that allow interfacing with the UPS, do the following:
```
sudo apt-get update
sudo apt-get install apcupsd
```

We will also need to configure the APC UPS daemon to work with our set up. Edit /etc/apcupsd/apcupsd.conf and change out the follow values like so:
```
#UPSCABLE smart
UPSCABLE usb

#UPSTYPE apcsmart
UPSTYPE usb

#DEVICE /dev/ttyS0
DEVICE
```

To make these changes go into effect, restart the service like so:
```
sudo systemctl restart apcupsd
```

Now you may install the link like normal, and you will have access to your UPS.

