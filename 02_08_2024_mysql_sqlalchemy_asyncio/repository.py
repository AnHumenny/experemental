from sqlalchemy import text, select, update, insert, delete
from database import DCreateUser, DCreateCountry, new_session


class Repo:
    @classmethod
    async def view_all_name(cls):
        async with new_session() as session:
            query = select(DCreateUser.name, DCreateUser.full_name)
            result = await session.execute(query)
            answer = result.scalars().all()
            await session.commit()
            await session.close()
            return answer

    #по идентификатору
    @classmethod
    async def view_person(cls, ssid):
        async with new_session() as session:
            q = select(DCreateUser.full_name).where(DCreateUser.id == text(ssid))
            result = await session.execute(q)
            answer = result.scalars()
            await session.close()
            return answer

    #инфо по всем user | project
    @classmethod
    async def view_all(cls, temp):
        async with new_session() as session:
            if temp == "user":
                q = select(DCreateUser.id, DCreateUser.name, DCreateUser.full_name, DCreateUser.age)
            if temp == "project":
                q = select(DCreateCountry.id, DCreateCountry.map, DCreateCountry.location, DCreateCountry.name)
            result = await session.execute(q)
            await session.close()
            return result

    # по локации
    @classmethod
    async def view_location(cls, location):
        async with new_session() as session:
            q = select(DCreateCountry.location, DCreateCountry.map).filter(DCreateCountry.name == location)
            result = await session.execute(q)
            answer = result.all()
            await session.close()
            return answer

    #update user | project
    @classmethod
    async def update_all_info(cls, l, temp):
        async with new_session() as session:
            if temp == "user":
                q = update(DCreateUser).where(DCreateUser.id == l[0]).values(l)
            if temp == "project":
                q = update(DCreateCountry).where(DCreateCountry.id == l[0]).values(l)
            await session.execute(q)
            await session.commit()
            await session.close()
            return

    #insert into User | Project
    @classmethod
    async def insert_into_all(cls, l, temp):
        async with new_session() as session:
            if temp == "user":
                q = insert(DCreateUser).values(l)
            if temp == "project":
                q = insert(DCreateCountry).values(l)
            await session.execute(q)
            await session.commit()
            await session.close()
            return True

    # deleted по идентификатору in Users
    @classmethod
    async def delete_all_id(cls, ssid, temp):
        async with new_session() as session:
            if temp == "user":
                q = delete(DCreateUser).where(DCreateUser.id == text(ssid))
            if temp == "project":
                q = delete(DCreateCountry).where(DCreateCountry.id == text(ssid))
            await session.execute(q)
            await session.commit()
            await session.close()
            return ("Deleted !")

    #поиск по возрасту
    @classmethod
    async def search_age(cls, symbol, age):
        async with new_session() as session:
            # q = select(DCreateUser.full_name).where(DCreateUser.age > 20)  #рабочий
            if symbol == ">":
                q = select(DCreateUser.full_name).where(DCreateUser.age > age)
            if symbol == "<":
                q = select(DCreateUser.full_name).where(DCreateUser.age < age)
            if symbol == "=":
                q = select(DCreateUser.full_name).where(DCreateUser.age == age)
        result = await session.execute(q)  #рабочий
        answer = result.scalars().all()
        await session.commit()
        await session.close()
        return answer
