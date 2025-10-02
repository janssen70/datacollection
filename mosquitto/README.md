# Mosquitto

Install mosquitto:

```sh
sudo apt install mosquitto
```

make sure `/etc/mosquitto/mosquitto.conf` contains

```
listen 1883
```

That's it. Assuming the MQTT safely takes place inside the VPN no
security precautions are necessary.

## Configure Axis devices

On Axis devices the following needs to be configured

- [MQTT broker connection](https://help.axis.com/en-us/axis-os-knowledge-base#mqtt)
- Event topics to publish
- Enable MQTT

A script is present that reads device address, username and password
combinations from an Excel file and then adjusts the MQTT settings for each
of those:

```sh
python3 setup_devices.py -f <excel filename> -b <mqtt broker address> [-t <topic to publish>]
```

For example, this publishes only a single event on MQTT:

```sh
python3 setup_devices.py -f devices.xlsx -b 192.168.200.102 -t onvif:AudioSource/axis:TriggerLevel
```

## Forward device publications into Openobserve

Adjust the provided `mqtt_to_o2.service` to the local situation and run:

```sh
sudo cp mqtt_to_o2.service /etc/systemd/system
sudo systemctl start mqtt_to_o2
sudo systemctl status mqtt_to_o2
sudo systemctl enable mqtt_to_o2
```

Fix any problems along the way
