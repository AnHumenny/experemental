from fastapi import HTTPException
from sqlalchemy import select, update, insert
import sqlalchemy
from project.shemas import SProject, SProjectId, SProjectUpdate, SProjectDelete, SProjectUpdateName
from employees.shemas import SEmployees, SEmployeesId, SDeleteUser, SUpdateSEmployeesId
from auth.shemas import SUser
from database import DEmployment, DProject, DUsers, new_session


class Repository:
    #insert в  Employees
    @classmethod
    async def insert_into_employees(cls, data: SEmployees):
        async with new_session() as session:
            task_dict = data.model_dump()
            task = DEmployment(**task_dict)
            session.add(task)
            await session.commit()
            await session.close()
            return task.id

    # insert в  Project
    @classmethod
    async def insert_into_project(cls, data: SProject):
        async with new_session() as session:
            task_dict = data.model_dump()
            task = DProject(**task_dict)
            session.add(task)
            await session.commit()
            await session.close()
            return task.id

    # тестовое INSERT по ПРЯМОМУ ЗАПРОСУ  в  Project
    @classmethod
    async def ins_project(cls, data: SProjectUpdate):
        async with new_session() as session:
            task = data.model_dump()
            ssid = task.get('id')
            print(ssid)
            # query = sqlalchemy.update(DProject).where(data.id == ssid).values(**task) #почти рабочий вариант))
            query = await session.execute(insert(DProject).values(**task))  # рабочий вариант
            print("query", query)
            if not query:
                raise HTTPException(status_code=404, detail="Object not found")
            await session.commit()
            await session.close()
            return

    # view by id в  Employees
    @classmethod
    async def sel_us(cls, data: SEmployeesId):
        async with new_session() as session:
            result = await session.get(DEmployment, data.id)
            if not result:
                raise HTTPException(status_code=404, detail="Object not found")
            await session.close()
            return result

    # view by id в  Project
    @classmethod
    async def sel_project(cls, data: SProjectId):
        async with new_session() as session:
            result = await session.get(DProject, data.id)
            if not result:
                raise HTTPException(status_code=404, detail="Object not found")
            await session.close()
            return result

    #тестовое выбрать конкретные поля по  id в  Project (доработать возврат значений)
    @classmethod
    async def project_concr(cls):
        async with new_session() as session:
            query = sqlalchemy.select(sqlalchemy.text('id, name')).select_from(
                sqlalchemy.text('project'))  #.where(data.id == 3)
            result = await session.execute(query)
            await session.commit()
            await session.close()
            return result

    # delete by id в  Project
    @classmethod
    async def project_delete(cls, data: SProjectDelete):
        async with new_session() as session:
            delete_project = await session.get(DProject, data.id)
            if not delete_project:
                raise HTTPException(status_code=404, detail="Object not found!")
            await session.delete(delete_project)
            await session.commit()
            await session.close()
            return {'object': data.id, 'info': 'the object was deleted!'}

    # delete by id в  Employees
    @classmethod
    async def delete_user(cls, data: SDeleteUser):
        async with new_session() as session:
            delete_person = await session.get(DEmployment, data.id)
            if not delete_person:
                raise HTTPException(status_code=404, detail="Object not found!")
            await session.delete(delete_person)
            await session.commit()
            await session.close()
            return {'object': data.id, 'info': 'the object was deleted!'}

    #получить все Project
    @classmethod
    async def get_all_project(cls):
        async with new_session() as session:
            query = select(DProject)
            result = await session.execute(query)
            if not result:
                raise HTTPException(status_code=404, detail="Object not found")
            task_models = result.scalars().all()
            await session.close()
            return task_models

    # получить все Users
    @classmethod
    async def get_all_users(cls):
        async with new_session() as session:
            query = select(DUsers)
            result = await session.execute(query)
            if not result:
                raise HTTPException(status_code=404, detail="Object not found")
            task_models = result.scalars().all()
            print("task_models", task_models)
            await session.close()
            return task_models

    # update по  id в  Project
    @classmethod
    async def update_project_id(cls, data: SProjectUpdate):
        async with new_session() as session:
            task = data.model_dump()
            stmt = (
                update(DProject).where(DProject.id == data.id).values(**task)  #.select.last_insert_id(DProject)
            )
            await session.execute(stmt)
            await session.commit()
            await session.close()
            return task

    # update по  name в  Project
    @classmethod
    async def update_project_name(cls, data: SProjectUpdateName):
        async with new_session() as session:
            task = data.model_dump()
            stmt = (
                update(DProject).where(DProject.name == data.name).values(**task)  # .select.last_insert_id(DProject)
            )
            await session.execute(stmt)
            await session.commit()
            await session.close()
            return {'id': task, 'info': 'Updated!'}

    # update по  id в  Employees
    @classmethod
    async def update_user(cls, data: SUpdateSEmployeesId):
        async with new_session() as session:
            task = data.model_dump()
            stmt = (
                update(DEmployment).where(DEmployment.id == data.id).values(**task)  # .select.last_insert_id(DProject)
            )
            await session.execute(stmt)
            await session.commit()
            await session.close()
            return {'id': task, 'info': 'Updated!'}


class Authentication:
    @classmethod
    async def sel_auth_user(cls, data: SUser):
        async with new_session() as session:
            task = data.model_dump()
            print(task)
            stmt = (
                select(DUsers).where(DUsers.login == data.login).values(**task)
            )
            await session.execute(stmt)
            await session.commit()
            print(stmt)
            if not stmt:
                raise HTTPException(status_code=404, detail="Object not found")
            await session.close()
            return True

