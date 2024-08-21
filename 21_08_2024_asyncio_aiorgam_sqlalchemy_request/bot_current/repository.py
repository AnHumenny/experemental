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


    @classmethod
    async def insert_into_date(cls, l):
        async with new_session() as session:
            q = insert(DCurrent).values(l)
            await session.execute(q)
            await session.commit()
            await session.close()
            return
            

    @classmethod
    async def insert_into_ctat_current(cls, l):
        async with new_session() as session:
            q = insert(DStat).values(l)
            await session.execute(q)
            await session.commit()
            await session.close()
            return

