import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

# from schema import EventUp as SchemaEvent
# from schema import EventUp
# from models import EventUp as ModelEventUp

from enum import Enum 
from fastapi import FastAPI, Path, Query

from contextlib import asynccontextmanager
from app.routers import gateway_manage, localization

from fastapi.middleware.cors import CORSMiddleware

# from services.gateway_manage import gateway_manage, localization_engine

import os
# from dotenv import load_dotenv

# load_dotenv('.env')

app = FastAPI()
app = FastAPI()
app.include_router(gateway_manage.router)
app.include_router(localization.router)

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url='postgresql://chirpstack_integration:chirpstack_integration@143.89.144.31/chirpstack_integration')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "hello world"}

@app.get('/author/')
async def author():
    author = db.session.query(ModelEventUp).all()
    return author

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload = True)

