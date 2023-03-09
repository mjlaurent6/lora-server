import json
import threading
from typing import Union

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import uvicorn

from app.mqtt_client import MQTTClient
from app.config import settings
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.encoders import jsonable_encoder

from app.models import GatewayMessage, EndDeviceMessage
app = FastAPI()

global_client = None

def on_message(client, userdata, msg):
    msg_dict = json.loads(msg.payload.decode())
    # TODO: validate message before inserting to db
    new_status = app.mongodb["db-test"].insert_one(msg_dict)
    # created_task = app.mongodb["db-test"].find_one(
    #     {"_id": new_status.inserted_id}
    # )

    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

@app.on_event("startup")
async def startup_db_client():
    global global_client
    print("Startup!")
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]
    # create mqtt client
    mqtt_client = MQTTClient("broker.emqx.io", 1883, app.mongodb)
    global_client = mqtt_client
    mqtt_client.subscribe('gateway/control/eui/command', on_message)
    # sub_thread = threading.Thread(target=mqtt_client.subscribe('gateway/control/eui/command', on_message))
    # sub_thread.start()
    # sub_thread.join()

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

@app.get("/status")
def get_items():
    return {"message": "ok"}

@app.get("/force_start")
def force_start():
    global_client.force_start()
    return {"message": "OK"}

@app.get("/force_stop")
def force_stop():
    global_client.force_stop()
    return {"message": "OK"}