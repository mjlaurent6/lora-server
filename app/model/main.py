import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

reloaded = tf.keras.models.load_model('rssi_to_distance')

def calculate_rssi_to_distance(payload: dict):
    data = pd.DataFrame(payload, index=[0])
    print(reloaded.predict(data)[0][0])
