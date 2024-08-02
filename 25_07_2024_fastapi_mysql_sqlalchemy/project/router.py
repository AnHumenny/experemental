from fastapi import APIRouter, Depends, Security
from typing import Annotated, Union
from auth.router import get_current_active_user, oauth2_scheme, get_current_user
from auth.shemas import SUser, SUserInDB
from project.shemas import SProject, SProjectId, SProjectDelete, SProjectUpdate, SProjectUpdateName
from repository import Repository

router = APIRouter(
    prefix="/info"
)



#выбрать всё в Project
@router.get("/select_all_project/")
async def select_project_project():
    result = await Repository.get_all_project()
    return {"info project": result}



#выбрать в Project по id
@router.get("/select_project/{id}")
async def select_project(
        ssid: Annotated[SProjectId, Depends()]
):
    result = await Repository.sel_project(ssid)
    return {"info project": result}


#добавить в Project
@router.post("/select_project/{id}")
async def insert_project(
        data: Union[SProject, Annotated[SUser, Depends()]]
):
    task = await Repository.insert_into_project(data)
    return {"info": task}



#выбрать в Project(недоработка с выводом логики обработки информации)
@router.get("/select_project_concr")
async def select_project(
):
    result = await Repository.project_concr()
    return {"info project": result}


#удалить в Project
@router.delete("/select_project_delete/{id}")
async def select_project(
        ssid: Annotated[SProjectDelete, Depends()]
):
    result = await Repository.project_delete(ssid)
    return {"info project": result}


#обновить в Project по id
@router.put("/update_project_id/{id}")
async def update_project_id(
        ssid: Annotated[SProjectUpdate, Depends()]
):
    result = await Repository.update_project_id(ssid)
    return {"info project": result}


#добавить в Project по name
@router.put("/update_project_name/{name}")
async def update_project_name(
        name: Annotated[SProjectUpdateName, Depends()]
):
    result = await Repository.update_project_name(name)
    return {"info project": result}
