import numpy as np
import json
from math import radians, cos, sin, asin, sqrt, atan2, degrees
from models import gateway_localize_model,Signal 
from fewella import algos

from typing import List

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

class Localization_Engine():
    PREFIX_TRAIN_DATA = 'train_data/processed'
    train_data = {}

    def __init__(self) -> None:
        self.reloaded = tf.keras.models.load_model('model/rssi_to_distance')
        with open(f'{self.PREFIX_TRAIN_DATA}/t8_tx10.json', 'r') as f1, open(f'{self.PREFIX_TRAIN_DATA}/t20_tx10.json') as f2, open(f'{self.PREFIX_TRAIN_DATA}/t8_tx15.json', 'r') as f3:
            data_str = json.load(f1)
            data = json.loads(data_str)
            self.train_data['rssi'] = data['rssi']
            self.train_data['distance'] = data['distance']
            print(len(self.train_data['rssi']))

    # convert rssi to distance/radius, by linear interpolating training data
    # def rssi_distance(self, rssi: float, tx_power: int = 10):
    #     # get first index, at which rssi from training data is lower than the given rssi value
    #     rssi_data = np.array(self.train_data['rssi'])
    #     distance = np.array(self.train_data['distance'])
    #     idx = np.argmax(rssi_data < rssi)
    #     # Generalized De-Moive's linear interpolation 
    #     # m = (y_1-y_0)/(x_1 - x_0)
    #     slope = (rssi_data[idx] - rssi_data[idx - 1])/(distance[idx] - distance[idx - 1])
    #     # (y - y_0) = m * (x - x_0) => x = (y - y_0)/m + x_0, where x is radius
    #     radius = (rssi - rssi_data[idx - 1])/slope + distance[idx - 1]
    #     print(f'interpolating between {distance[idx - 1]} and {distance[idx]}')
    #     print('radius:', radius)
    #     return radius/1000

    # -30rssi @ 1m
    n = [1.96, 2.829, 2.79]
    A = [-29, -25, -20]
    def rssi_to_distance(self, rssi, i = 0):
        dist = 10 ** ((self.A[i] - rssi) / (10 * self.n[i]))
        return dist

    def calculate_rssi_to_distance(self, payload: Signal):
        data = {'rssi': float(payload.rssi), 'snr': float(payload.snr), 'tx_power': float(payload.tx_power)}
        data = pd.DataFrame(data, index=[0])
        result = self.reloaded.predict(data)[0]
        return result[0]
        # return self.reloaded.predict(data)[0][0]

    def localize(self, gateways: List[gateway_localize_model]):
        # convert geometric coordinate system to cartesian coordinates
        gateway_input = []

        # set first gateway as (0, 0)
        ref_long = gateways[0].longitude
        ref_lat = gateways[0].lattitude
        gateway_input.append((0, 0, self.rssi_distance(gateways[0].rssi)))
        gateways.pop(0)

        for g in gateways:
            print(g.lattitude, g.longitude)
            # calculate distance between current gateway and reference/first gateway
            d = self.distance(ref_lat, g.lattitude, ref_long, g.longitude)
            print(d)
            bearing = radians(self.calc_bearing(ref_lat, ref_long, g.lattitude, g.longitude))
            # measure relative distance between reference gateway and current gateway in (x, y)
            x = sin(bearing) * d
            y = cos(bearing) * d
            r = self.rssi_distance(g.rssi)

            gateway_input.append((x, y, r))

        print(gateway_input)

        (target_x, target_y) = algos.maximum_likelihood(gateway_input)
        angle = degrees(atan2(target_x, target_y))
        distance = sqrt(x**2 + y**2)

        return self.get_point_at_distance(ref_lat, ref_long, distance, angle)


    def calc_bearing(self, lat1, long1, lat2, long2):
        # Convert latitude and longitude to radians
        lat1 = radians(lat1)
        long1 = radians(long1)
        lat2 = radians(lat2)
        long2 = radians(long2)
        
        # Calculate the bearing
        bearing = atan2(
            sin(long2 - long1) * cos(lat2),
            cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(long2 - long1)
        )
        
        # Convert the bearing to degrees
        bearing = degrees(bearing)
        
        # Make sure the bearing is positive
        bearing = (bearing + 360) % 360
        
        return bearing
    

    def get_point_at_distance(self, lat1, lon1, d, bearing, R=6371):
        """
        lat: initial latitude, in degrees
        lon: initial longitude, in degrees
        d: target distance from initial
        bearing: (true) heading in degrees
        R: optional radius of sphere, defaults to mean radius of earth

        Returns new lat/lon coordinate {d}km from initial, in degrees
        """
        lat1 = radians(lat1)
        lon1 = radians(lon1)
        a = radians(bearing)
        lat2 = asin(sin(lat1) * cos(d/R) + cos(lat1) * sin(d/R) * cos(a))
        lon2 = lon1 + atan2(
            sin(a) * sin(d/R) * cos(lat1),
            cos(d/R) - sin(lat1) * sin(lat2)
        )
        return (degrees(lat2), degrees(lon2),)

    

    # Python 3 program to calculate Distance Between Two Points on Earth
    
    def distance(self, lat1, lat2, lon1, lon2):
        # The math module contains a function named
        # radians which converts from degrees to radians.
        lon1 = radians(lon1)
        lon2 = radians(lon2)
        lat1 = radians(lat1)
        lat2 = radians(lat2)
        
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    
        c = 2 * asin(sqrt(a))
        
        # Radius of earth in kilometers. Use 3956 for miles
        r = 6371
        
        # calculate the result
        return(c * r)