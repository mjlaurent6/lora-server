import os
import datetime
import json
import subprocess
import time


delta_read_time = 5


def follow(filename):
    f = open(filename, "r")
    f.seek(0, 2)  # Go to the end of the file
    while True:
        line = f.readline()
        if not line:
            yield -1
        else:
            yield line


def extract_rssi(json_payload):
    data = json.loads(json_payload)
    rssi = data["data"]["rx_metadata"][0]["rssi"]
    return rssi


def get_most_recent_rssi(output_filename):
    f = open(output_filename, "r")
    rssis = []
    prev  = ""
    json_payload = ""
    for line in f:
        json_end = len(line) == 1 and "{" not in prev
        if json_end:
            try:
                rssi = extract_rssi(json_payload)
                rssis.append(rssi)
            except:
                rssi = 0
            json_payload = ""
        
        else:
            json_payload += line
        
        prev = line
    
    return rssis[-1]


if __name__ == "__main__":
    
    output_filename = "colin-test"

    cmd_login           =  "ttn-lw-cli login"
    cmd_gateway_traffic = f"ttn-lw-cli events --gateway-id afewell-gateway > {output_filename}"
    
    login_proc = subprocess.Popen(cmd_login, shell=True, stdout=subprocess.PIPE)
    login_proc.wait()

    proc = subprocess.Popen([cmd_gateway_traffic], shell=True, stdin=None, stdout=None, stderr=None)
    time.sleep(1)

    output_file = "output.txt"
    distance = ''
    while True:
        # Gather input from user
        print('Distance:')
        distance = input()
        # break when quit is entered
        if distance.lower() == 'quit':
            break
        # create string
        rssi = get_most_recent_rssi(output_filename)
        s = str(datetime.datetime.now()) + ',' + str(distance) + ',' + str(rssi) + '\n'
        print(s, end='')
        # save to text file
        f = open('output.txt', 'a')
        f.write(s)
        f.close()
