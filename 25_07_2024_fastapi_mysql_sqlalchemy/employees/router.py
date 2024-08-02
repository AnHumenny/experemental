import token

from fastapi import APIRouter, Depends
from typing import Annotated
from employees.shemas import SEmployees, SEmployeesId, SDeleteUser, SUpdateSEmployeesId

from repository import Repository


router = APIRouter(
    prefix="/info"
)


#добавить в Employees
@router.post("/insert_into/employees")
async def insert_employeement(
        data: Annotated[SEmployees, Depends()]
):
    task = await Repository.insert_into_employees(data)
    return {"info": task}


#выбрать в Employees
@router.get("/select_id_new/{id}")
async def select_id(
        ssid: Annotated[SEmployeesId, Depends()]
):
    ssid = await Repository.sel_us(ssid)
    return {"info": ssid}


#удалить по id
@router.delete("/delete_user_id/{id}")
async def delete_user(
        ssid: Annotated[SDeleteUser, Depends()]
):
    result = await Repository.delete_user(ssid)
    return {"info": result}


#update по id
@router.put("/update_user_id/{id}")
async def delete_user(
        ssid: Annotated[SUpdateSEmployeesId, Depends()]
):
    result = await Repository.update_user(ssid)
    return {"info": result}
