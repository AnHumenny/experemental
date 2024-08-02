from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker



engine = create_async_engine(
    "mysql+asyncmy://db_user:db_password@localhost/orm_test"
)

new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class DEmployment(Model):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    phone = Column(Integer)
    email = Column(String(50))
    area_of_responsibility = Column(String(250))
    post = Column(String(20))
    category = Column(Integer)


class DProject(Model):
    __tablename__ = "project"
    name = Column(String(50))
    location = Column(String(50))
    participants = Column(String(220))
    cost = Column(Integer)
    id = Column(Integer, primary_key=True)


class DUsers(Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    full_name = Column(String(50))
    email = Column(String(50))
    hashed_password = Column(String(50))
    disabled = Column(Boolean, unique=False, default=True)







