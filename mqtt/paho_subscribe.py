import context 
import paho.mqtt.subscribe as subscribe

# follow installations section of https://pypi.org/project/paho-mqtt/, before running this script
# topics used by application server can be found in https://www.thethingsindustries.com/docs/integrations/mqtt/

# constants taken from ttn mqtt integrations dashboard
application_id = 'gch6-lora-test1@ttn'
device_id = 'eui-ac1f09fffe08dec1-steven'
hostname = 'nam1.cloud.thethings.network'
username = 'gch6-lora-test1@ttn'
password = 'NNSXS.K4JDRU5A373PJRFALPGX2BT6XATZ36OWBHKLWPY.47CBOLGJVYRHMJYJALCUR5VN6HIODY42VOBTSWO75EX2JN6D4CWA'

def on_message_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))

# subscribe.callback(on_message_print, topics=[f"v3/{application_id}/devices/{device_id}/down/ack"], hostname=hostname, port=1883, auth={'username':username,'password':password})

m = subscribe.simple(topics=[f"v3/{application_id}/devices/{device_id}/down/ack", f'v3/{application_id}/devices/{device_id}/down/failed', f'v3/{application_id}/devices/{device_id}/down/sent', f'v3/{application_id}/devices/{device_id}/down/queued'], hostname=hostname, port=1883, auth={'username':username,'password':password}, msg_count=2)
for a in m:
    print(a.topic)
    print(a.payload)

# subscribe command using mosquitto mqtt client
#    mosquitto_sub -h nam1.cloud.thethings.network -t "#" -u "gch6-lora-test1@ttn" -P "NNSXS.K4JDRU5A373PJRFALPGX2BT6XATZ36OWBHKLWPY.47CBOLGJVYRHMJYJALCUR5VN6HIODY42VOBTSWO75EX2JN6D4CWA" -d
