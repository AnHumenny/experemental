from sqlalchemy import Column, Integer, String, Date, BOOLEAN, DateTime
from datetime import datetime
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(
    "mysql+asyncmy://user:password@localhost/database"
)


new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class DCurrent(Model):
    __tablename__ = "current"
    id = Column(Integer, primary_key=True, autoincrement=True)
    actual_current = Column(String(15))
    date = Column(DateTime, default=datetime.utcnow)
    type_current = Column(String(5))


class DUser(Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(30))
    name = Column(String(30))
    status = Column(String(15))
    password = Column(BOOLEAN)
    phone = Column(String(14))
    email = Column(String(50))
    tg_id = Column(String(50))

class DStat(Model):
    __tablename__ = "stat_current"
    id = Column(Integer, primary_key=True, autoincrement=True)
    actual_current = Column(String(15))
    date = Column(Date, default=datetime.utcnow)
    type_current = Column(String(5))
