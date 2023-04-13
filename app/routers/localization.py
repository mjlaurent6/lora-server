from fastapi import APIRouter, Query
from pydantic import Required
from typing_extensions import Annotated
import json
import numpy as np

from models import gateway_localize_model, gateway_rssi_in, gateway_rssi_out, Signal
from typing import List
from util.localization_engine import Localization_Engine

router = APIRouter(prefix='/localization')
engine = Localization_Engine()

@router.post('/distance')
async def get_radius(gateways: List[gateway_rssi_in]):
    out = []
    res = []
    for g in gateways:
        est_distance = engine.calculate_rssi_to_distance(g.signal)
        signal = Signal(rssi=100, tx_power=100, snr=100)
        # print(signal)
        result = gateway_rssi_out(
            device_eui=g.device_eui,
            gateway_eui=g.gateway_eui,
            signal=signal,
            distance=est_distance
        )
        res.append(result)
    return res

@router.post('/trilaterate')
async def localize(gateways: List[gateway_localize_model] = Required):
    # TODO: Try to use fewell's localization algorithm
    return engine.localize(gateways)
    
