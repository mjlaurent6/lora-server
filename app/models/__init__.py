import uuid
from typing import Union
from pydantic import BaseModel, Field


class EndDeviceMessage(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    dev_eui: str = ""
    payload: Union[str, None] = None
    gateway_eui: str = ""

class GatewayMessage(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    dev_eui: str = ""
    payload: Union[str, None] = None
