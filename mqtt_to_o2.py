import json
import time
import requests
import os
import paho.mqtt.client as mqtt

IP_ADDRESS = '192.168.2.95'
# MQTT broker settings
MQTT_BROKER = IP_ADDRESS
MQTT_PORT = 1883
MQTT_TOPIC = 'axis/+/event/tns:onvif/#'

# OpenObserve ingest endpoint + auth
OO_URL = f'http://{IP_ADDRESS}:5080/api/default/ingest/metrics/_json'
OO_USER = os.getenv('ZO_ROOT_USER_EMAIL')
OO_PASS = os.getenv('ZO_ROOT_USER_PASSWORD')

if not OO_USER or not OO_PASS:
    print('Configure Openobserve credentials first')
    exit(-1)

# Prepare a requests session for efficiency
session = requests.Session()
session.auth = (OO_USER, OO_PASS)
session.headers.update({'Content-Type': 'application/json'})

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected to MQTT broker')
        client.subscribe(MQTT_TOPIC)
    else:
        print('Failed to connect, return code', rc)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode('utf-8'))

        # Extract "container" from MQTT topic (2nd part)
        topic_parts = msg.topic.split('/')
        container = topic_parts[1] if len(topic_parts) > 1 else 'unknown'

        # Convert payload -> OpenObserve metric
        metric = {
            '__name__': 'audio_input',
            '__type__': 'gauge',
            'namespace': 'audio',
            'container': container,
            # Use camera timestamp if present, otherwise fallback
            '_timestamp': int(payload.get('timestamp', time.time() * 1e6)),
            'value': int(payload.get('message', {}).get('data', {}).get('triggered', '0'))
        }

        print('Uploading metric:', metric)

        # Post to OpenObserve (OO expects a JSON array of metrics)
        resp = session.post(OO_URL, json=[metric])
        if resp.status_code != 200:
            print(f'Upload failed: {resp.status_code} {resp.text}')

    except Exception as e:
        print('Error handling message:', e)

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

if __name__ == '__main__':
    main()
