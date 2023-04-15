from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, ARRAY, JSON
from sqlalchemy.ext.declarative import declarative_base

from pydantic import BaseModel, dataclasses, Field
from dataclasses import field
from typing import Union
from enum import Enum

Base  = declarative_base()

class gateway_commands: 
    PREFIX = '/gateway/control'
    PING = 'ping'
    REBOOT = 'reboot'
    START = 'start'
    STOP = 'stop'
    TEMP = 'temp'
    UPTIME = 'uptime'

class remote_request(Enum):
    REBOOT = 0
    START = 1
    STOP = 2

# define models here
@dataclasses.dataclass
class data_payload():
    temp: Union[float, None] = None
    uptime: Union[float, None] = None
    feedback: Union[str, None] = None
    # msg: str

@dataclasses.dataclass
class gateway_out_model():
    gateway_eui: str
    elpased_time: float
    exception: Union[str, None] = None
    payload: Union[data_payload, None] = None

@dataclasses.dataclass
class Signal():
    rssi: float
    snr: float
    # remove later
    tx_power: float = 15

@dataclasses.dataclass
class Location():
    altitude: float = None
    latitude: float = None
    longitude: float = None

class base_gateway_model(BaseModel):
    gateway_id: str
    signal: Signal

class gateway_localize_model(base_gateway_model):
    latitude: float
    longitude: float
    rssi: float

class gateway_rssi_in(base_gateway_model):
    pass

class gateway_rssi_out(base_gateway_model):
    location: Location
    distance: float