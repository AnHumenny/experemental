
from fastapi import APIRouter, Depends
from typing import Annotated

from shemas import SStatDayTypeCurrent, SStatDayCurrent

from repository import Stat


router = APIRouter(
    prefix="/info"
)


#выбрать последние 7 по type_current
@router.get("/view_course")
async def select_info(
        data: Annotated[SStatDayTypeCurrent, Depends()]
):
    task = await Stat.get_current(data)
    return {"info": task}

#выбрать последние date
@router.get("/view_date")
async def select_info(
        data: Annotated[SStatDayCurrent, Depends()]
):
    task = await Stat.get_current_date(data)
    return {"info": task}
