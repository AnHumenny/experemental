from sqlalchemy import select, insert
from create_db.database import DGazprom, DManual, DUser, DVisitedUser, DBaseStation, new_session


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
    async def select_azs(cls, number):
        async with new_session() as session:
            q = select(DGazprom).where(DGazprom.number == number)
            result = await session.execute(q)
            answer = result.scalar()
            await session.close()
            return answer

    @classmethod
    async def select_manual(cls, ssid):
        async with new_session() as session:
            q = select(DManual).where(DManual.id == ssid)
            result = await session.execute(q)
            answer = result.scalar()
            await session.close()
            return answer

    @classmethod
    async def insert_into_date(cls, l):
        async with new_session() as session:
            q = insert(DVisitedUser).values(l)
            await session.execute(q)
            await session.commit()
            await session.close()
            return

    @classmethod
    async def select_action(cls, number):
        async with new_session() as session:
            query = select(DVisitedUser).order_by(DVisitedUser.id.desc()).limit(int(number))
            result = await session.execute(query)
            answer = result.scalars().all()
            await session.close()
            return answer


    @classmethod
    async def select_bs_number(cls, number):
        async with new_session() as session:
            query = select(DBaseStation).where(DBaseStation.number == int(number))
            result = await session.execute(query)
            answer = result.scalar()
            await session.commit()
            await session.close()
            return answer

    @classmethod
    async def select_bs_address(cls, address):
        async with new_session() as session:
            query = select(DBaseStation).where(DBaseStation.address.like(f"%{address}%"))
            result = await session.execute(query)
            answer = result.scalars()
            await session.commit()
            await session.close()
            return answer
