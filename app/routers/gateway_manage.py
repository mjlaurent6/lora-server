from fastapi import APIRouter, Query, Depends, Request, status, Response
from typing_extensions import Annotated

from util.mqtt import MQTTClient
from util import parser
from dependencies import gateway_query_params

import asyncio
from concurrent.futures import ThreadPoolExecutor
from models import *

# initialize required objects
MAX_TIMEOUT = 1
mqtt = MQTTClient('broker.emqx.io',1883)
executor = ThreadPoolExecutor(5)
router = APIRouter(prefix=gateway_commands.PREFIX, dependencies=[Depends(gateway_query_params)])

# listens for feedback from gateway through mqtt 
async def listen(eui):
    event_loop = asyncio.get_event_loop()
    # run in new thread
    future = event_loop.run_in_executor(executor, lambda: mqtt.sub_and_wait(f'{gateway_commands.PREFIX}/{eui}', MAX_TIMEOUT))
    response, elapsed_time = await future
    if response is None:
        raise TimeoutError('Response took too long!', elapsed_time)
    return response, elapsed_time

    
@router.get("/ping", status_code=status.HTTP_200_OK)
async def ping(request: Request, response: Response):
    # publish to mqtt  topic
    mqtt.publish(f'{gateway_commands.PREFIX}/{request.state.eui}', gateway_commands.PING)
    #await response from gateway
    try:
        response, elapsed_time = await listen(request.state.eui)
    except TimeoutError as e:
        print('Response took too long')
        response.status_code = status.HTTP_408_REQUEST_TIMEOUT
        return gateway_out_model(request.state.eui, e.args[1], exception=e.args[0])
    
    return gateway_out_model(request.state.eui, elapsed_time)

@router.get('/reboot', status_code=status.HTTP_200_OK)
async def reboot(request: Request, config_file: str, server_address: str, response: Response):
    # publish to mqtt topic 
    mqtt.publish(f'{gateway_commands.PREFIX}/{request.state.eui}', gateway_commands.REBOOT)

    try:
        response, elapsed_time = await listen(request.state.eui)
    except TimeoutError as e:
        print('Response took too long')
        response.status_code = status.HTTP_408_REQUEST_TIMEOUT
        return gateway_out_model(request.state.eui, e.args[1], exception=e.args[0])
    
    return gateway_out_model(request.state.eui, elapsed_time, payload=data_payload(feedback=response.payload))

@router.get('/start', status_code=status.HTTP_200_OK)
async def start(request: Request, config_file: str, server_address: str):
    mqtt.publish(f'{gateway_commands.PREFIX}/{request.state.eui}', f'{gateway_commands.START};{config_file};{server_address}')

    try:
        response, elapsed_time = await listen(request.state.eui)
    except TimeoutError as e:
        print('Response took too long')
        response.status_code = status.HTTP_408_REQUEST_TIMEOUT
        return gateway_out_model(request.state.eui, e.args[1], exception=e.args[0])
    
    return gateway_out_model(request.state.eui, elapsed_time, payload=data_payload(feedback=response.payload)) 

@router.get('/stop', status_code=status.HTTP_200_OK)
async def stop(request: Request, config_file: str, server_addres: str):
    mqtt.publish(f'{gateway_commands.PREFIX}/{request.state.eui}', f'{gateway_commands.STOP};{config_file};{server_addres}')
    try:
        response, elapsed_time = listen(request.state.eui)
    except TimeoutError as e:
        print('Response took too long')
        response.status_code = status.HTTP_408_REQUEST_TIMEOUT
        return gateway_out_model(request.state.eui, e.args[1], exception=e.args[0])
    
    return gateway_out_model(request.state.eui, elapsed_time, payload=data_payload(feedback=response.payload))

@router.get('/temp', status_code=status.HTTP_200_OK)
async def get_temp(request: Request):
    # publish to mqtt  topic
    mqtt.publish(f'{gateway_commands.PREFIX}/{request.state.eui}', gateway_commands.TEMP)

    # await response from gateway
    try:
        response, elapsed_time = listen(request.state.eui)
    except TimeoutError as e:
        print('Response took too long')
        response.status_code = status.HTTP_408_REQUEST_TIMEOUT
        return gateway_out_model(request.state.eui, e.args[1], exception=e.args[0])
    
    temp = parser.parse_temp(response.payload)
    return gateway_out_model(request.state.eui, elapsed_time, payload = data_payload(temp=temp))

@router.get('/uptime', status_code=status.HTTP_200_OK)
async def get_uptime(request: Request):
     # publish to mqtt  topic
    mqtt.publish(f'{gateway_commands.PREFIX}/{request.state.eui}', gateway_commands.UPTIME)

    # await response from gateway
    try:
       response, elapsed_time = listen(request.state.eui)
    except TimeoutError as e:
        print('Response took too long')
        response.status_code = status.HTTP_408_REQUEST_TIMEOUT
        return gateway_out_model(request.state.eui, e.args[1], exception=e.args[0])
    
    uptime = parser.parse_uptime(response.payload)
    return gateway_out_model(request.state.eui, elapsed_time, payload = data_payload(uptime=uptime))
