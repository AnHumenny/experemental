import psycopg2
from config import host, password, user

def create_database(dtb):
    # Подключение к PostgreSQL
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database="postgres"
    )
    try:
        with conn.cursor() as cursor:
            conn.autocommit = True
            sql = f"CREATE DATABASE {dtb}"
            cursor.execute(sql)
            print(f"База {dtb} данных успешно создана")
    except (Exception, psycopg2.Error) as error:
        print(f"Ошибка при работе с PostgreSQL: {error}")
        return
    finally:
        conn.commit()
        conn.close()

def view_database():
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database="postgres"
    )
    conn.autocommit = True
    sql = f"SELECT datname FROM pg_database"
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
        return result
    except (Exception, psycopg2.Error) as error:
        print(f"Ошибка при работе с PostgreSQL: {error}")
    finally:
        conn.commit()
        conn.close()


def drop_database(dtb):
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database="postgres"
    )
    conn.autocommit = True
    try:
        with conn.cursor() as cursor:
            sql = f"DROP DATABASE {dtb}"
            cursor.execute(sql)
            result = cursor.fetchall()
        return result
    except (Exception, psycopg2.Error) as error:
       print(f"\nОшибка при работе с PostgreSQL: {error}база данных {dtb} отсутствует")
       return
    finally:
        conn.commit()
        conn.close()

def view_table_database(dtb):
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=dtb
    )
    conn.autocommit = True
    sql = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
        return result
    except (Exception, psycopg2.Error) as error:
        print(f"\nОшибка при работе с PostgreSQL: {error}база данных {dtb} отсутствует")
        return
    finally:
        conn.commit()
        conn.close()

def view_structure(dtb, table_name):
    conn = psycopg2.connect(
        host=host,
        database=dtb,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
        fields = [column[0] for column in cursor.description]
        return fields
    except (Exception, psycopg2.Error) as error:
        print(f"Ошибка при работе с PostgreSQL: {error} данные не найдены")
    finally:
        conn.commit()
        conn.close()


def view_role(dtb):
    conn = psycopg2.connect(
        host=host,
        database=dtb,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT rolname, rolcanlogin, rolsuper, rolinherit, rolcreaterole, rolcreatedb, rolbypassrls, rolconnlimit FROM pg_roles")
        users = cursor.fetchall()
        return users
    except (Exception, psycopg2.Error) as error:
        print(f"Ошибка при работе с PostgreSQL: {error} данные не найдены")
    finally:
        conn.commit()
        conn.close()


def view_user():
    conn = psycopg2.connect(
        host=host,
        database="postgres",
        user=user,
        password=password,
    )
    cur = conn.cursor()
    cur.execute("SELECT usename FROM pg_user")
    try:
        users = cur.fetchall()
        return users
    except (Exception, psycopg2.Error) as error:
        print(f"Ошибка при работе с PostgreSQL: {error} пользователи не найдены")
    finally:
        conn.commit()
        conn.close()


def drop_table(dtb, table):
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=dtb
    )
    cur = conn.cursor()
    try:
        cur.execute(f'DROP TABLE IF EXISTS {table};')
        return f'Таблица {table} успешно удалена'
    except (Exception, psycopg2.Error) as error:
       return f"Ошибка при работе с PostgreSQL: {error}база данных {dtb} отсутствует"
    finally:
        cur.close()
        conn.commit()
        conn.close()
