from fastapi import HTTPException
from sqlalchemy import select, insert
from create_db.database import DStat, DUser, DCurrent, new_session


class Repo:
    @classmethod
    async def select_pass(cls, login, password, tg_id):
        async with new_session() as session:
            q = select(DUser).where(DUser.login == login, DUser.password == password, DUser.tg_id == tg_id)
            result = await session.execute(q)
            answer = result.scalar()
            await session.close()
            return answer

    # insert into User | Project
    @classmethod
    async def insert_into_date(cls, l):
        async with new_session() as session:
            print("l", l)
            q = insert(DCurrent).values(l)
            await session.execute(q)
            await session.commit()
            await session.close()
            return

    @classmethod
    async def insert_into_ctat_current(cls, l):
        async with new_session() as session:
            print("l", l)
            q = insert(DStat).values(l)
            await session.execute(q)
            await session.commit()
            await session.close()
            return

    @classmethod
    async def select_current(cls, insert_type):
        async with new_session() as session:
            query = select(DStat).where(DStat.type_current == insert_type).order_by(DStat.id.desc()).limit(4)
            result = await session.execute(query)
            if not result:
                raise HTTPException(status_code=404, detail="Object not found")
            answer = result.scalars().all()
            await session.close()
            return answer
