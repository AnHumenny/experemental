
from sqlalchemy import select, insert
from create_db.database import DGazprom, DManual, DUser, DVisitedUser, new_session


class Repo:
    #авторизация
    @classmethod
    async def select_pass(cls, login, password):
        async with new_session() as session:
            print(login)
            q = select(DUser).where(DUser.login == login, DUser.password == password)
            result = await session.execute(q)
            answer = result.scalar()
            await session.close()
            return answer

    
    # select from DGazprom по номеру АЗС
    @classmethod
    async def select_azs(cls, number):
        async with new_session() as session:
            print(number)
            q = select(DGazprom).where(DGazprom.number == number)
            result = await session.execute(q)
            answer = result.scalar()
            await session.close()
            return answer

    # select from DManual по id 
    @classmethod
    async def select_manual(cls, ssid):
        async with new_session() as session:
            q = select(DManual).where(DManual.id == ssid)
            result = await session.execute(q)
            answer = result.scalar()
            await session.close()
            return answer

    # insert DVisitedUser
    @classmethod
    async def insert_into_date(cls, l):
        async with new_session() as session:
            q = insert(DVisitedUser).values(l)
            await session.execute(q)
            await session.commit()
            await session.close()
            return
    
    #select from DVisitedUser 
    @classmethod
    async def select_action(cls, number):
        async with new_session() as session:
            query = select(DVisitedUser).order_by(DVisitedUser.id.desc()).limit(int(number))
            result = await session.execute(query)
            answer = result.scalars().all()
            await session.close()
            return answer
