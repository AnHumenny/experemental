from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase


class Model(DeclarativeBase):
    pass


class DUser(Model):
    __tablename__ = f"_user"
    id = Column(Integer, index=True, primary_key=True)
    login = Column(String(30))
    full_name = Column(String(40))
    age = Column(Integer)
    position = Column(String(30))
    cash = Column(Integer)
 

class DCustomer(Model):
    __tablename__ = f"_customer"
    id = Column(Integer, index=True, primary_key=True)
    product = Column(String(40))
    quantity = Column(Integer)
    amount = Column(Integer)




