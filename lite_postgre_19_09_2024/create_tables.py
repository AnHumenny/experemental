from database import DUser, DCustomer
import config
import db_operation
from sqlalchemy import create_engine

def create_table():     #создание таблиц
    dtbs = db_operation.Pg(host=config.host, port=config.port, user=config.user,
                                password=config.password, database=config.database)
    question = input("создаём новую? Y/N: ")
    if question == "Y":
        dtb = input("enter database: ")
        dtbs.create_database(dtb)
        engine = create_engine(
            f"postgresql://{config.user}:{config.password}@{config.host}/{dtb}", echo=True
        )
        q = input("добавляем таблицы? Y/N: ")
        if q == "Y": 
            DUser.metadata.create_all(engine)        #пример
            DCustomer.metadata.create_all(engine)     #пример

    else:
        database = input("имя существующей БД: ")
        engine = create_engine(
            f"postgresql://{config.user}:{config.password}@{config.host}/{database}", echo=True
            )
        DUser.metadata.create_all(engine)     #пример
        DCustomer.metadata.create_all(engine)  #пример


