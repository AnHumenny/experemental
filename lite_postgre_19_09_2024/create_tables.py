from database import DUser, DCustomer
from config import host, user, password
from db_operation import create_database
from sqlalchemy import create_engine

def create_table():
    question = input("создаём новую? Y/N: ")
    if question == "Y":
        dtb = input("enter database: ")
        create_database(dtb)
        engine = create_engine(
            f"postgresql://{user}:{password}@{host}/{dtb}", echo=True
        )
        q = input("добавляем таблицы? Y/N: ")
        if q == "Y":
            DUser.metadata.create_all(engine)
            DCustomer.metadata.create_all(engine)
    else:
        database = input("имя существующей БД: ")
        engine = create_engine(
            f"postgresql://{user}:{password}@{host}/{database}", echo=True
            )
        DUser.metadata.create_all(engine)
        DCustomer.metadata.create_all(engine)

