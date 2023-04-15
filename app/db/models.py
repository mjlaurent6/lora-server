# coding: utf-8
from sqlalchemy import BigInteger, Boolean, CHAR, Column, DateTime, Float, LargeBinary, SmallInteger, String, Text, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class DieselSchemaMigration(Base):
    __tablename__ = '__diesel_schema_migrations'

    version = Column(String(50), primary_key=True)
    run_on = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class EventAck(Base):
    __tablename__ = 'event_ack'

    queue_item_id = Column(UUID, primary_key=True)
    deduplication_id = Column(UUID, nullable=False)
    time = Column(DateTime(True), nullable=False)
    tenant_id = Column(UUID, nullable=False)
    tenant_name = Column(Text, nullable=False)
    application_id = Column(UUID, nullable=False)
    application_name = Column(Text, nullable=False)
    device_profile_id = Column(UUID, nullable=False)
    device_profile_name = Column(Text, nullable=False)
    device_name = Column(Text, nullable=False)
    dev_eui = Column(CHAR(16), nullable=False)
    tags = Column(JSONB(astext_type=Text()), nullable=False)
    acknowledged = Column(Boolean, nullable=False)
    f_cnt_down = Column(BigInteger, nullable=False)


class EventIntegration(Base):
    __tablename__ = 'event_integration'

    deduplication_id = Column(UUID, primary_key=True)
    time = Column(DateTime(True), nullable=False)
    tenant_id = Column(UUID, nullable=False)
    tenant_name = Column(Text, nullable=False)
    application_id = Column(UUID, nullable=False)
    application_name = Column(Text, nullable=False)
    device_profile_id = Column(UUID, nullable=False)
    device_profile_name = Column(Text, nullable=False)
    device_name = Column(Text, nullable=False)
    dev_eui = Column(CHAR(16), nullable=False)
    tags = Column(JSONB(astext_type=Text()), nullable=False)
    integration_name = Column(Text, nullable=False)
    event_type = Column(Text, nullable=False)
    object = Column(JSONB(astext_type=Text()), nullable=False)


class EventJoin(Base):
    __tablename__ = 'event_join'

    deduplication_id = Column(UUID, primary_key=True)
    time = Column(DateTime(True), nullable=False)
    tenant_id = Column(UUID, nullable=False)
    tenant_name = Column(Text, nullable=False)
    application_id = Column(UUID, nullable=False)
    application_name = Column(Text, nullable=False)
    device_profile_id = Column(UUID, nullable=False)
    device_profile_name = Column(Text, nullable=False)
    device_name = Column(Text, nullable=False)
    dev_eui = Column(CHAR(16), nullable=False)
    tags = Column(JSONB(astext_type=Text()), nullable=False)
    dev_addr = Column(CHAR(8), nullable=False)


class EventLocation(Base):
    __tablename__ = 'event_location'

    deduplication_id = Column(UUID, primary_key=True)
    time = Column(DateTime(True), nullable=False)
    tenant_id = Column(UUID, nullable=False)
    tenant_name = Column(Text, nullable=False)
    application_id = Column(UUID, nullable=False)
    application_name = Column(Text, nullable=False)
    device_profile_id = Column(UUID, nullable=False)
    device_profile_name = Column(Text, nullable=False)
    device_name = Column(Text, nullable=False)
    dev_eui = Column(CHAR(16), nullable=False)
    tags = Column(JSONB(astext_type=Text()), nullable=False)
    latitude = Column(Float(53), nullable=False)
    longitude = Column(Float(53), nullable=False)
    altitude = Column(Float(53), nullable=False)
    source = Column(Text, nullable=False)
    accuracy = Column(Float, nullable=False)


class EventLog(Base):
    __tablename__ = 'event_log'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('event_log_id_seq'::regclass)"))
    time = Column(DateTime(True), nullable=False)
    tenant_id = Column(UUID, nullable=False)
    tenant_name = Column(Text, nullable=False)
    application_id = Column(UUID, nullable=False)
    application_name = Column(Text, nullable=False)
    device_profile_id = Column(UUID, nullable=False)
    device_profile_name = Column(Text, nullable=False)
    device_name = Column(Text, nullable=False)
    dev_eui = Column(CHAR(16), nullable=False)
    tags = Column(JSONB(astext_type=Text()), nullable=False)
    level = Column(Text, nullable=False)
    code = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    context = Column(JSONB(astext_type=Text()), nullable=False)


class EventStatu(Base):
    __tablename__ = 'event_status'

    deduplication_id = Column(UUID, primary_key=True)
    time = Column(DateTime(True), nullable=False)
    tenant_id = Column(UUID, nullable=False)
    tenant_name = Column(Text, nullable=False)
    application_id = Column(UUID, nullable=False)
    application_name = Column(Text, nullable=False)
    device_profile_id = Column(UUID, nullable=False)
    device_profile_name = Column(Text, nullable=False)
    device_name = Column(Text, nullable=False)
    dev_eui = Column(CHAR(16), nullable=False)
    tags = Column(JSONB(astext_type=Text()), nullable=False)
    margin = Column(SmallInteger, nullable=False)
    external_power_source = Column(Boolean, nullable=False)
    battery_level_unavailable = Column(Boolean, nullable=False)
    battery_level = Column(Float, nullable=False)


class EventTxAck(Base):
    __tablename__ = 'event_tx_ack'

    queue_item_id = Column(UUID, primary_key=True)
    downlink_id = Column(BigInteger, nullable=False)
    time = Column(DateTime(True), nullable=False)
    tenant_id = Column(UUID, nullable=False)
    tenant_name = Column(Text, nullable=False)
    application_id = Column(UUID, nullable=False)
    application_name = Column(Text, nullable=False)
    device_profile_id = Column(UUID, nullable=False)
    device_profile_name = Column(Text, nullable=False)
    device_name = Column(Text, nullable=False)
    dev_eui = Column(CHAR(16), nullable=False)
    tags = Column(JSONB(astext_type=Text()), nullable=False)
    f_cnt_down = Column(BigInteger, nullable=False)
    gateway_id = Column(CHAR(16), nullable=False)
    tx_info = Column(JSONB(astext_type=Text()), nullable=False)


class EventUp(Base):
    __tablename__ = 'event_up'

    deduplication_id = Column(UUID, primary_key=True)
    time = Column(DateTime(True), nullable=False)
    tenant_id = Column(UUID, nullable=False)
    tenant_name = Column(Text, nullable=False)
    application_id = Column(UUID, nullable=False)
    application_name = Column(Text, nullable=False)
    device_profile_id = Column(UUID, nullable=False)
    device_profile_name = Column(Text, nullable=False)
    device_name = Column(Text, nullable=False)
    dev_eui = Column(CHAR(16), nullable=False)
    tags = Column(JSONB(astext_type=Text()), nullable=False)
    dev_addr = Column(CHAR(8), nullable=False)
    adr = Column(Boolean, nullable=False)
    dr = Column(SmallInteger, nullable=False)
    f_cnt = Column(BigInteger, nullable=False)
    f_port = Column(SmallInteger, nullable=False)
    confirmed = Column(Boolean, nullable=False)
    data = Column(LargeBinary, nullable=False)
    object = Column(JSONB(astext_type=Text()), nullable=False)
    rx_info = Column(JSONB(astext_type=Text()), nullable=False)
    tx_info = Column(JSONB(astext_type=Text()), nullable=False)
