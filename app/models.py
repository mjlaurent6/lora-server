from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, ClauseList, ARRAY, JSON
from sqlalchemy.ext.declarative import declarative_base

from pydantic import BaseModel, dataclasses, Field
from dataclasses import field
from typing import Union

Base  = declarative_base()


class EventUp(Base):
    __tablename__ = 'event_up'
    deduplication_id = Column(String, primary_key=True, index=True)
    device_name = Column(String)
    rx_info = Column(ARRAY(JSON))
    tx_info = Column(ARRAY(JSON))

class gateway_commands: 
    PREFIX = '/gateway/control'
    PING = 'PING'
    REBOOT = 'REBOOT'
    START = 'START'
    STOP = 'STOP'
    TEMP = 'TEMP'
    UPTIME = 'UPTIME'

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
    tx_power: float
    snr: float

class base_gateway_model(BaseModel):
    gateway_eui: str
    device_eui: str
    signal: Signal

class gateway_localize_model(base_gateway_model):
    lattitude: float
    longitude: float
    rssi: float

class gateway_rssi_in(base_gateway_model):
    pass

class gateway_rssi_out(base_gateway_model):
    distance: float

