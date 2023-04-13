from fastapi import Query, Request
from pydantic import Required
from typing_extensions import Annotated

from util.mqtt import MQTTClient

# Put all dependecies here, authorization, db, etc

class gateway_query_params:
    def __init__(self, request: Request, eui: Annotated[str, Query(regex='^0x', max_length=12)] = Required):
        request.state.eui = eui


