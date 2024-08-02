from time import sleep
import mysql.connector
from sqlalchemy import create_engine
from database import DCreateUser, DCreateCountry


user = input('user: ')   #условно прилетает извне
password = input('password: ')  #условно прилетает извне
db_name = input('db_name: ')  # input("имя создаваемой/удаляемой базы/просмотр - просто Enter: ") #условно прилетает извне


engi = create_engine(
    f"mysql+pymysql://{user}:{password}@localhost/{db_name}"
)


def view_database():
    l = []
    mydb = mysql.connector.connect(host="localhost", user=f"{user}", password=f"{password}")
    cursor = mydb.cursor()
    sql = "SHOW DATABASES"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        l.append(*row)
    print(l)
    mydb.close()


def create_base():
    mydb = mysql.connector.connect(host="localhost", user=f"{user}", password=f"{password}")
    cursor = mydb.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    print("Ok!")
    sleep(3)
    DCreateUser.metadata.create_all(engi)
    DCreateCountry.metadata.create_all(engi)
    print(f"database {db_name} is created!")
    mydb.close()
    view_database()


def delete_base():
    mydb = mysql.connector.connect(host="localhost", user=f"{user}", password=f"{password}")
    cursor = mydb.cursor()
    drop_sql = f"DROP DATABASE IF EXISTS {db_name}"
    cursor.execute(drop_sql)
    mydb.close()
    view_database()


def start_action():
    query = input("create|delete|view: ")
    if query == "create":
        create_base()
    if query == "delete":
        delete_base()
    if query == "view":
        view_database()


start_action()

