from fastapi import APIRouter, Query, Depends
from pydantic import Required
from typing_extensions import Annotated
import json
import numpy as np

from app.models import gateway_localize_model, gateway_rssi_in, gateway_rssi_out, Signal, Location
from typing import List
from app.util.localization_engine import Localization_Engine
from sqlalchemy.orm import Session

from app.database import SessionLocal, db_engine
from sqlalchemy import desc

from app.db.models import EventUp

router = APIRouter(prefix='/localization')
engine = Localization_Engine()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/distance')
async def get_radius(device_eui: str, db: Session = Depends(get_db), limit: int = 5):
    event_ups = db.query(EventUp).filter(EventUp.dev_eui == device_eui).order_by(desc(EventUp.time)).limit(limit).all()
    out = []
    res = []

    for event in event_ups:
        gateways = event.rx_info
        gateway_listener = []
        for gateway in gateways:
            s = Signal(rssi=gateway['rssi'], tx_power=15, snr=gateway['snr'])
            est_distance = engine.calculate_rssi_to_distance(s)
            signal = Signal(rssi=gateway['rssi'], tx_power=15, snr=gateway['snr'])
            if gateway.get('location') and gateway['location'].get('altitude'):
                location = Location(
                    altitude=gateway['location']['altitude'],
                    longitude=gateway['location']['longitude'],
                    latitude=gateway['location']['latitude']
                )
            else:
                location = Location()
            # print(signal)
            result = gateway_rssi_out(
                gateway_id=gateway['gatewayId'],
                signal=signal,
                location=location,
                distance=est_distance
            )
            gateway_listener.append(result)
        event_result = {
            'time': event.time,
            'rx_info': gateway_listener,
        }
        res.append(event_result)
    # for g in gateways:
    #     # print(g.rx_info[0])
    #     s = Signal(rssi=g.rx_info[0]['rssi'], tx_power=15, snr=g.rx_info[0]['snr'])
    #     est_distance = engine.calculate_rssi_to_distance(s)
    #     signal = Signal(rssi=g.rx_info[0]['rssi'], tx_power=15, snr=g.rx_info[0]['snr'])
    #     if g.rx_info[0].get('location') and g.rx_info[0]['location'].get('altitude'):
    #         location = Location(
    #             altitude=g.rx_info[0]['location']['altitude'],
    #             longitude=g.rx_info[0]['location']['longitude'],
    #             latitude=g.rx_info[0]['location']['latitude']
    #         )
    #     else:
    #         location = Location()
    #     # print(signal)
    #     result = gateway_rssi_out(
    #         device_eui=g.dev_eui,
    #         gateway_eui=g.rx_info[0]['gatewayId'],
    #         signal=signal,
    #         location=location,
    #         distance=est_distance
    #     )
    #     res.append(result)
    return res

@router.post('/trilaterate')
async def localize(gateways: List[gateway_localize_model] = Required):
    # TODO: Try to use fewell's localization algorithm
    return engine.localize(gateways)
    
