# datacollection

A bunch of scripts and configuration files to help collect data from a number of Axis devices. Data collected is:

- Syslog
- Event occurences published on mqtt
- (todo) Log of http requests

It uses these tools:

  - Openobserve
  - AxoSyslog
  - Mosquitto
  - Several Python scripts:
    - mqtt_to_02: listen to mqtt and push into Openobserve
    - <tbd>: configure mqtt connection on devices

The requirements that led to this choice were:

- Open source, free, self-managed versions of commercial solutions
- Deployable on both Linux and Windows (through WSL)
- Small footprint (small VM or bare metal)
- Act as remote syslog endpoint for Axis devices
- Allow sufficient options for data collection to help collect event conditions outside of syslog context
- Be able to query the data later, on criteria not yet known

The files provided here work for me. You will need to adapt IP addresses, pathnames, usernames and so on to your own situation.

<!-- # mqtt_to_02

Quick & dirty, ChatGPT assisted, script to subscribe to "axis/+/event/tns:onvif/#" and push into Openobserve metrics endpoint -->

## Getting started
Easiest way to get started is to clone this repo in a user root folder, e.g. `/home/erik` so that you end up with `/home/erik/datacollection`. 
This isn't mandatory, just less paths to change to make things work. Read the various `README.md` files to get started with each of the tools. 
The file settings.env and the individual service files need to be adapted to the local situation. 
