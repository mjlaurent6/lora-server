import context
import paho.mqtt.publish as publish

# follow installations section of https://pypi.org/project/paho-mqtt/, before running this script

# constants taken from ttn mqtt integrations dashboard
application_id = 'gch6-lora-test1@ttn'
device_id = 'eui-ac1f09fffe08dec1-steven'
hostname = 'nam1.cloud.thethings.network'
username = 'gch6-lora-test1@ttn'
password = 'NNSXS.K4JDRU5A373PJRFALPGX2BT6XATZ36OWBHKLWPY.47CBOLGJVYRHMJYJALCUR5VN6HIODY42VOBTSWO75EX2JN6D4CWA' # API KEY 

publish.single(f"v3/{application_id}/devices/{device_id}/down/push", '{"downlinks":[{"f_port": 15,"frm_payload":"vu8=","priority": "NORMAL"}]}', hostname="nam1.cloud.thethings.network", port=1883, auth={'username':username,'password':password})