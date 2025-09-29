# datacollection

A bunch of scripts to help collect data from a number of Axis devices. It uses

  - Openobserve
  - AxoSyslog
  - Mosquitto
  - Several Python scripts:
    - mqtt_to_02: listen to mqtt and push into Openobserve
    - <tbd>: configure mqtt connection on devices



# mqtt_to_02

Quick & dirty, ChatGPT assisted, script to subscribe to "axis/+/event/tns:onvif/#" and push into Openobserve metrics endpoint
