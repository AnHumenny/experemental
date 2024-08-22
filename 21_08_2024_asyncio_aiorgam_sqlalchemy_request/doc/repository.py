from fastapi import HTTPException
from database import DStat, new_session
from sqlalchemy import select, update, insert
from shemas import SStatDayTypeCurrent, SStatDayCurrent


class Stat:

    @classmethod
    async def get_current(cls, data: SStatDayTypeCurrent):
        async with new_session() as session:
            query = select(DStat).where(DStat.type_current == data.type_current).order_by(DStat.id.desc()).limit(7)
            result = await session.execute(query)
            if not result:
                raise HTTPException(status_code=404, detail="Object not found")
            task_models = result.scalars().all()
            await session.close()
            return task_models


    @classmethod
    async def get_current_date(cls, data: SStatDayCurrent):
        async with new_session() as session:
            query = select(DStat).where(DStat.date == data.date).order_by(DStat.id.desc()).limit(4)
            result = await session.execute(query)
            if not result:
                raise HTTPException(status_code=404, detail="Object not found")
            task_models = result.scalars().all()
            await session.close()
            return task_models
