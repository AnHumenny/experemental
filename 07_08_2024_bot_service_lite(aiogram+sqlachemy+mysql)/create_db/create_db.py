from time import sleep
import pymysql
import mysql.connector
from database import DGazprom, DManual, DUser, DVisitedUser, DBaseStation
from sqlalchemy import create_engine

#
user = "admin" #input('user: ')   #условно прилетает извне
password = "1qazxcde3"  # input('password: ')  #условно прилетает извне
db_name = "orm_3" #input("имя создаваемой/удаляемой базы/просмотр - просто Enter: ") #условно прилетает извне


engine = create_engine(
    f"mysql+pymysql://admin:1qazxcde3@localhost/{db_name}"
)


def show_database():
    l = []
    conn = pymysql.connect(host="localhost", user=user, password=password)
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    result = cursor.fetchall()
    for row in result:
        l.append(row)
    print(l)
    if db_name not in l:
        create_base()
        sleep(3)
        create_tables()
        print("Ok!")
    if db_name in l:
        create_tables()
    conn.commit()
    conn.close()


def create_base():
    mydb = mysql.connector.connect(host="localhost", user=f"{user}", password=f"{password}")
    cursor = mydb.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    print(f"Ok! {db_name} created!")


def create_tables():
    DGazprom.metadata.create_all(engine)
    DManual.metadata.create_all(engine)
    DUser.metadata.create_all(engine)
    DVisitedUser.metadata.create_all(engine)
    DBaseStation.metadata.create_all(engine)
    print("Ok! Tables created!")


show_database()
