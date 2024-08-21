from sqlalchemy import insert, select
from create_db.database import DStat, new_session


class Repo:
    @classmethod
    async def insert_into_ctat_current(cls, l):
        async with new_session() as session:
            q = insert(DStat).values(l)
            await session.execute(q)
            await session.commit()
            await session.close()
            return

    @classmethod
    async def select_current(cls, type_current):
        async with new_session() as session:
            q = select(DStat).where(DStat.type_current == type_current).order_by(DStat.id.desc()).limit(7)
            result = await session.execute(q)
            answer = result.scalars()
            await session.close()
            return answer

