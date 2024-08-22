from datetime import datetime
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


engine = create_async_engine(
    "mysql+asyncmy://user:password@localhost/database"
)


new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class DStat(Model):
    __tablename__ = "stat_current"
    id = Column(Integer, primary_key=True, autoincrement=True)
    actual_current = Column(String(15))
    date = Column(Date, default=datetime.utcnow)
    type_current = Column(String(5))
