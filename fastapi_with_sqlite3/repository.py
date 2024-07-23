from database import DBaseOrm, new_session
from shemas import (SPerson, SSelectCourse, SSelectMajor, SSelectEnrollmentYear, SSelectStatus, SUpdatePerson,
                    SDeletePerson)
import sqlite3
from sqlalchemy.sql import text


path_to_db = "base.db"
path_to_table = "main"


class Repository:
    @classmethod
    async def insert_into(cls, data: SPerson):
        async with new_session() as session:
            person_dict = data.model_dump()
            task = DBaseOrm(**person_dict)
            print('таска', task)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id

    @classmethod
    async def update_person(cls, data: SUpdatePerson):
        async with new_session() as session:
            person_dict = data.model_dump()
            ssid = person_dict.get('id')
            name = person_dict.get('name')
            await session.execute(text(f'''UPDATE INTO {path_to_table} SET name = ? WHERE ssid = ?''', (name, ssid))) #ошибка синтаксиса, доработать
            await session.flush()
            await session.commit()
            return




class Repo:
    @classmethod
    async def select_course(cls, data: SSelectCourse):
        data = data.model_dump()
        temp_data = data.get('course')
        conn = sqlite3.connect(path_to_db)
        cursor = conn.execute(f'''SELECT id, name, full_name, phone FROM {path_to_table}
                              WHERE status = ? AND course = ?''', ('student', temp_data))
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        return result

    @classmethod
    async def select_major(cls, data: SSelectMajor):
        data = data.model_dump()
        temp_data = data.get('major')
        conn = sqlite3.connect(path_to_db)
        cursor = conn.execute(f'''SELECT id, name, full_name, phone FROM {path_to_table} WHERE 
        status = ? AND  major = ?''',('student', temp_data))
        result = cursor.fetchall()
        conn.close()
        return result

    @classmethod
    async def select_enrollment_year(cls, data: SSelectEnrollmentYear):
        date = data.model_dump()
        temp_data = date.get('enrollment_year')
        conn = sqlite3.connect(path_to_db)
        cursor = conn.execute(f'''SELECT name, full_name, date_of_birth, enrollment_year, course
                                FROM {path_to_table} WHERE status = ? AND enrollment_year = ? ''',
                                ('student', temp_data))
        result = cursor.fetchall()
        conn.close()
        return result

    @classmethod
    async def select_status(cls, data: SSelectStatus):
        data = data.model_dump()
        temp_data = data.get('status')
        conn = sqlite3.connect(path_to_db)
        cursor = conn.execute(f'''SELECT id, name, full_name, phone, status FROM {path_to_table}
                              WHERE status = ? ''', (temp_data, ))
        result = cursor.fetchall()
        conn.close()
        return result

    @classmethod
    async def delete_person(cls, data: SDeletePerson):
        data = data.model_dump()
        temp_data = data.get('id')
        conn = sqlite3.connect(path_to_db)
        cursor = conn.cursor()
        print("Подключен к SQLite")
       # sql_delete_query = f"""DELETE from {path_to_table} where id = {temp_data}"""
        sql_delete_query = f"""DELETE from {path_to_table} where id = {temp_data}"""
        cursor.execute(sql_delete_query)
        conn.commit()
        print("Запись успешно удалена")
        cursor.close()
        return


    @classmethod
    async def update_person(cls, data: SUpdatePerson):
        data = data.model_dump()
        temp_data = data.get('id')
        name = data.get('name')
        conn = sqlite3.connect(path_to_db)
        cursor = conn.cursor()
        print("Подключен к SQLite")
        #sql_update_query = f"""UPDATE {path_to_table} set name = {full_name} where id = {temp_data} """
        sql_update_query = f"""UPDATE {path_to_table} SET name = {name} where id = {temp_data} """  #почему то в name проходят только числовые значения, доработать
        cursor.execute(sql_update_query)
        conn.commit()
        print("Запись успешно добавлена")
        cursor.close()
        return
