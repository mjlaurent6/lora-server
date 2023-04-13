from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, ClauseList, ARRAY, JSON
from sqlalchemy.ext.declarative import declarative_base

Base  = declarative_base()


class EventUp(Base):
    __tablename__ = 'event_up'
    deduplication_id = Column(String, primary_key=True, index=True)
    device_name = Column(String)
    rx_info = Column(ARRAY(JSON))
    tx_info = Column(ARRAY(JSON))



