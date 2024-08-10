
from sqlalchemy import Column, Integer, String, Text, BOOLEAN
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(
    "mysql+asyncmy://user:password@localhost/db_name"
)


new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class DGazprom(Model):
    __tablename__ = "gazprom"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(15))
    number = Column(String(10))
    address = Column(String(255))
    tip = Column(String(10))
    region = Column(String(100))
    comment = Column(String(500))
    geo = Column(String(30))


class DManual(Model):
    __tablename__ = "manual"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tip = Column(String(255))
    comment = Column(Text)


class DUser(Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(30))
    name = Column(String(30))
    status = Column(String(15))
    password = Column(BOOLEAN)    #подкорректировать в BLOB!!!
    phone = Column(String(14))
    email = Column(String(50))
    tg_id = Column(String(50))


class DVisitedUser(Model):
    __tablename__ = "visited_users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(30))
    date = Column(String(30))
    action = Column(String(50))


class DBaseStation(Model):
    __tablename__ = "base_station"
    id = Column(Integer, primary_key=True, autoincrement=True)
    comment = Column(String(255))
    address = Column(String(255))
    number = Column(Integer())
