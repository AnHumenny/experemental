from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(
    "mysql+asyncmy://db_user:db_password@localhost/orm_result"
)

new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class DCreateUser(Model):
    __tablename__ = "hhh_user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    full_name = Column(String(30))
    age = Column(Integer)


class DCreateCountry(Model):
    __tablename__ = "hhh_country"
    id = Column(Integer, primary_key=True, autoincrement=True)
    map = Column(String(30))
    location = Column(String(30))
    name = Column(String(30))


# async def create_table():
#     async with engine.begin() as conn:
#         await conn.run_sync(Model.metadata.create_all)


