from fastapi import APIRouter, Query, Depends
from pydantic import Required
from typing_extensions import Annotated
import json
import numpy as np

from app.routers.models import gateway_localize_model, gateway_rssi_in, gateway_rssi_out, Signal, Location
from typing import List
from app.services.localization_engine import localization_engine
from sqlalchemy.orm import Session

from sqlalchemy import desc
from app.db.models import EventUp
from app.dependencies import get_db

router = APIRouter(prefix='/localization')
engine = localization_engine()

@router.get('/distance')
async def get_radius(device_eui: str = Required, db: Session = Depends(get_db), limit: int = 5):
    # Query event_up records
    event_ups = db.query(EventUp).filter(EventUp.dev_eui == device_eui).order_by(desc(EventUp.time)).limit(limit).all()
    res = []
    for event in event_ups:
        gateways = event.rx_info
        gateway_listener = []
        for gateway in gateways:
            est_distance = engine.calculate_rssi_to_distance(**gateway)
            result = gateway_rssi_out(
                gateway_id=gateway['gatewayId'],
                signal=Signal(**gateway),
                location=Location(**gateway['location']),
                distance=est_distance
            )
            gateway_listener.append(result)
        event_result = {
            'time': event.time,
            'rx_info': gateway_listener,
        }
        res.append(event_result)
    return res

@router.post('/trilaterate')
async def trilaterate(gateways: List[gateway_localize_model] = Required):
    # TODO: Try to use fewell's localization algorithm
    return engine.trilaterate(gateways)
    
