import json

# Define methods for parsing gateway response here
def parse_temp(payload):
    data = json.loads(payload)
    temp_float = float(data['temp'])
    print(data['temp'])
    if temp_float > 100 or temp_float < 0:
        raise ValueError('Invalid temperature value')
    return temp_float
    
def parse_uptime(payload):
    data = json.loads(payload)
    uptime = float(data['uptime'])
    # TODO: Validate uptime before returning
    return uptime