import psycopg2
import config
from config import host, port, user, password, database
from psycopg2 import sql
import subprocess
import os
import pandas as pd
from sqlalchemy import create_engine

class Pg:
    def __init__(self, database, user, password, host, port):    #инициализация
        try:
            self.conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
            self.cursor = self.conn.cursor()
            print("Подключение к базе данных успешно.")
        except Exception as e:
            print(f"Ошибка подключения: {e}")

    def create_database(self, dtb):                       #создать базу
        self.conn.autocommit = True
        q = f"CREATE DATABASE {dtb}"
        try:
            self.cursor.execute(q)
            print(f"База {dtb} данных успешно создана")
        except (Exception, psycopg2.Error) as error:
            print(f"Ошибка при работе с PostgreSQL: {error}")
            return
        finally:
            self.cursor.close()
            self.conn.close()

    def view_database(self):                  #посмотреть список баз
        self.conn.autocommit = True
        q = f"SELECT datname FROM pg_database"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(q)
                result = cursor.fetchall()
                cursor.close()
            return result
        except (Exception, psycopg2.Error) as error:
            print(f"Ошибка при работе с PostgreSQL: {error}")
        finally:
            self.conn.close()

    def drop_database(self, dtb):             #удалить базу
        self.conn.autocommit = True
        q = f"DROP DATABASE {dtb}"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(q)
                result = cursor.fetchall()
            return result
        except (Exception, psycopg2.Error) as error:
            print(f"\nОшибка при работе с PostgreSQL: {error}база данных {dtb} отсутствует")
            return
        finally:
            self.cursor.close()
            self.conn.close()

    def view_table_database(self, dtb):        #посмотреть таблицы в базе
        conn = psycopg2.connect(
            host=host,
            database=dtb,
            user=user,
            password=password
        )
        conn.autocommit = True
        try:
            q = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
            with conn.cursor() as cursor:
                cursor.execute(q)
                result = cursor.fetchall()
                cursor.close()
            return result
        except (Exception, psycopg2.Error) as error:
            print(f"\nОшибка при работе с PostgreSQL: {error}база данных {dtb} отсутствует")
            return
        finally:
            conn.close()
            self.cursor.close()

    @staticmethod
    def view_structure(dtb, table_name):        #посмотреть структуру таблицы
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
            return None
        finally:
            conn.commit()
            conn.close()

    def view_role(self):                     #посмотреть роли пользователей
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "SELECT rolname, rolcanlogin, rolsuper, rolinherit, rolcreaterole, rolcreatedb, rolbypassrls, rolconnlimit FROM pg_roles")
            users = cursor.fetchall()
            return users
        except (Exception, psycopg2.Error) as error:
            print(f"Ошибка при работе с PostgreSQL: {error} данные не найдены")
            return None
        finally:
            cursor.close()
            self.conn.commit()
            self.conn.close()

    def view_user(self):                     #список пользователей
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT usename FROM pg_user")
            users = cursor.fetchall()
            return users
        except (Exception, psycopg2.Error) as error:
            print(f"Ошибка при работе с PostgreSQL: {error} пользователи не найдены")
        finally:
            cursor.close()
            self.conn.commit()
            self.conn.close()

    def drop_table(self, dtb, table):         #удалить таблицу
        cursor = self.conn.cursor()
        try:
            cursor.execute(f'DROP TABLE IF EXISTS {table};')
            return f'Таблица {table} успешно удалена'
        except (Exception, psycopg2.Error) as error:
            return f"Ошибка при работе с PostgreSQL: {error}база данных {dtb} отсутствует"
        finally:
            cursor.close()
            self.conn.commit()
            self.conn.close()

    def create_new_user(self, usr, pswrd):             #создать нового пользователя
        cursor = self.conn.cursor()
        try:
            create_user_query = sql.SQL("CREATE USER {} WITH PASSWORD %s;").format(sql.Identifier(usr))
            cursor.execute(create_user_query, (pswrd,))
            return f"Пользователь {usr} успешно создан."
        except Exception as e:
            print(f"Ошибка при создании пользователя: {e}")
        finally:
            cursor.close()
            self.conn.commit()
            self.conn.close()

    def delete_user(self, usr):               #удалить пользователя
        cursor = self.conn.cursor()
        try:
            delete_user_query = sql.SQL("DROP USER IF EXISTS {}").format(sql.Identifier(usr))
            cursor.execute(delete_user_query)
            return f"Пользователь '{usr}' успешно удален!"
        except Exception as e:
            return f"Ошибка при удалении пользователя: {e}"
        finally:
            cursor.close()
            self.conn.commit()
            self.conn.close()

    def grant_privileges(self, dtb, usr, privileges):      #предоставить права на БД
        try:
            self.cursor = self.conn.cursor()
            grant_query = f"GRANT {privileges} ON DATABASE {dtb} TO {usr};"
            self.cursor.execute(grant_query)
            return f"Успешно предоставлено {privileges} пользователю {usr} на базу данных {dtb}."
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        finally:
            self.cursor.close()
            self.conn.close()

    def grant_privileges_table(self, usr, dtb, table, privileges):    #предоставить права на таблицу
        conn_params = {
            'dbname': dtb,
            'user': user,
            'password': password,
            'host': host,
            'port': port
        }
        conn = psycopg2.connect(**conn_params)
        self.conn.autocommit = True
        q = f"GRANT {privileges} ON {table} TO {usr};"
        try:
            self.cursor = conn.cursor()
            self.cursor.execute(q)
            print(f"Привилегии на таблицу {table} были успешно предоставлены пользователю {usr}.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        finally:
            self.cursor.close()
            self.conn.close()

    @staticmethod
    def export_db_to_sql(db_name, output_file):
        conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host
        )
        cursor = conn.cursor()
        with open(output_file, 'w') as f:
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
            tables = cursor.fetchall()
            for table in tables:
                table_name = table[0]
                cursor.execute(
                    f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name='{table_name}'")
                columns = cursor.fetchall()
                f.write(f'-- Table: {table_name}\n')
                f.write(f'CREATE TABLE {table_name} (\n')
                for col in columns:
                    f.write(f'    {col[0]} {col[1]},\n')
                f.write(');\n\n')
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                for row in rows:
                    f.write(f"INSERT INTO {table_name} VALUES (")
                    f.write(', '.join(f"'{str(val)}'" for val in row))
                    f.write(');\n')
                f.write('\n')
                return True
        cursor.close()
        conn.close()

    @staticmethod                              #экспорт базы
    def export_database(db_name, output_file):
        os.environ['PGPASSWORD'] = config.password
        try:
            command = [
                'pg_dump',
                '--dbname=postgresql://{}:{}@{}:{}/{}'.format(config.user, config.password, config.host, config.port, db_name),
                '--file={}'.format('dump/' + output_file),
                '--no-owner',
                '--no-privileges'
            ]
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return "Экспорт завершен: {}".format('dump/' + output_file)
        except subprocess.CalledProcessError as e:
            return "Ошибка при экспорте базы данных: {}".format(e.stderr.decode())

    @staticmethod                              #экспорт таблицы
    def export_data_table(db_name, table_name, output_file):
        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
        df = pd.read_sql_table(table_name, con=engine)
        df.to_csv(f'dump/{output_file}.csv', index=False)
        return f'данные из таблицы  "{table_name}" экспортированы в  {output_file}.csv успешно!'


    @staticmethod                               #импорт таблицы
    def import_table(db_name, table_name, column, l, csv_file_path):
        try:
            conn = psycopg2.connect(
            host=host,
            database=db_name,
            user=user,
            password=password
            )
            cursor = conn.cursor()
            data = pd.read_csv(csv_file_path)
            for index, row in data.iterrows():
                insert_query = f"INSERT INTO {table_name} ({column}) VALUES ({l})"
                cursor.execute(insert_query, tuple(row))
            conn.commit()
            return "Данные успешно импортированы."
        except Exception as e:
            return f"Ошибка: {e}"
        finally:
            cursor.close()
            conn.close()
