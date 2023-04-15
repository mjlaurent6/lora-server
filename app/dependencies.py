from fastapi import Query, Request, Security, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from pydantic import Required
from typing_extensions import Annotated

from app.services.mqtt import MQTTClient
from app.db.database import SessionLocal
from app.config import Settings, get_settings

# Put all dependecies here, authorization, db, etc
# api_key auth
api_key_header = APIKeyHeader(name="API_KEY", auto_error=False)

class gateway_query_params:
    def __init__(self, request: Request, gateway_id: Annotated[str, Query(regex='^0x', max_length=24)] = Required):
        request.state.gateway_id = gateway_id

# db Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_api_key(settings: Settings = Depends(get_settings), api_key_header: str = Security(api_key_header)):
    if api_key_header == settings.api_key:
        return api_key_header   
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )