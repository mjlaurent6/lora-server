import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from schema import EventUp as SchemaEvent
from schema import EventUp
from models import EventUp as ModelEventUp




import os
# from dotenv import load_dotenv

# load_dotenv('.env')

app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url='postgresql://chirpstack_integration:chirpstack_integration@143.89.144.31/chirpstack_integration')


@app.get("/")
async def root():
    return {"message": "hello world"}

@app.get('/author/')
async def author():
    author = db.session.query(ModelEventUp).all()
    return author