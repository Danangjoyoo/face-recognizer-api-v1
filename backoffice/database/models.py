from email.policy import default
from typing import Optional
from sqlalchemy import (
    Column,
    Boolean,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Enum,
    INTEGER,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import backref, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import MetaData
from datetime import datetime
import enum

metadata = MetaData()

Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    time_created = Column(DateTime, default=datetime.now())

class Client(Base):
    __tablename__ = "client"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    key = Column(String(255), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    totalHit = Column(Integer)