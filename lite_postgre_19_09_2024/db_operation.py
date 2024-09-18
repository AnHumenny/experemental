import psycopg2
from config import host, password, user

def create_database(dtb):
    try:
        # Подключение к PostgreSQL
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database="postgres"
        )

        # Проверка наличия базы данных
        with conn.cursor() as cursor:
            conn.autocommit = True
            sql = f"CREATE DATABASE {dtb}"
            cursor.execute(sql)
            print(f"База {dtb} данных успешно создана")
        conn.close()
    except (Exception, psycopg2.Error) as error:
        print(f"Ошибка при работе с PostgreSQL: {error}")
    return


def view_database():
    try:
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database="postgres"
        )
        with conn.cursor() as cursor:
            conn.autocommit = True
            sql = f"SELECT datname FROM pg_database"
            cursor.execute(sql)
            result = cursor.fetchall()
        conn.close()
        return result
    except (Exception, psycopg2.Error) as error:
        print(f"Ошибка при работе с PostgreSQL: {error}")


def drop_database(dtb):
    try:
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database="postgres"
        )
        with conn.cursor() as cursor:
            conn.autocommit = True
            sql = f"DROP DATABASE {dtb}"
            cursor.execute(sql)
            result = cursor.fetchall()
        conn.close()
        return result
    except (Exception, psycopg2.Error) as error:
       print(f"Ошибка при работе с PostgreSQL: {error}база данных {dtb} отсутствует")
    return


def view_table_database(dtb):
    try:
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=dtb
        )
        with conn.cursor() as cursor:
            conn.autocommit = True
            sql = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
            cursor.execute(sql)
            result = cursor.fetchall()
        conn.close()
        return result
    except (Exception, psycopg2.Error) as error:
       print(f"Ошибка при работе с PostgreSQL: {error}база данных {dtb} отсутствует")
    return

def view_structure(dtb, table_name):
    try:
        conn = psycopg2.connect(
            host=host,
            database=dtb,
            user=user,
            password=password
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
        fields = [column[0] for column in cursor.description]
        conn.close()
        return fields
    except (Exception, psycopg2.Error) as error:
        print(f"Ошибка при работе с PostgreSQL: {error} данные не найдены")

def view_role(dtb, usr):
    conn = psycopg2.connect(
        host=host,
        database=dtb,
        user=usr,
        password=password
    )
    cursor = conn.cursor()
    # Получение списка пользователей и их прав
    cursor.execute(
        "SELECT rolname, rolcanlogin, rolsuper, rolinherit, rolcreaterole, rolcreatedb, rolbypassrls, rolconnlimit FROM pg_roles")
    users = cursor.fetchall()
    conn.close()
    return users


def view_user():
    conn = psycopg2.connect(
        host=host,
        database="postgres",
        user=user,
        password=password,
    )
    cur = conn.cursor()
    cur.execute("SELECT usename FROM pg_user")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users
