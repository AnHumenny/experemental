import sqlite3

from fastapi import APIRouter, Depends
from typing import Annotated
from shemas import (SPerson, SSelectCourse, SSelectMajor, SSelectEnrollmentYear, SSelectStatus, SUpdatePerson,
                    SDeletePerson)
from repository import Repository, Repo


router = APIRouter(
    prefix="/info"
)


@router.post("/insert_into")
async def insert_into(
        data: Annotated[SPerson, Depends()]
):
    task = await Repository.insert_into(data)
    return {"id": task, "data": data}


@router.get("/select_student/{course}")
async def select_course(
        course: Annotated[SSelectCourse, Depends()]

):
    task_course = await Repo.select_course(course)
    return {"course": course, "info": task_course}


@router.get("/select_major/{major}")
async def select_major(
        major: Annotated[SSelectMajor, Depends()]
):
    task_major = await Repo.select_major(major)
    return {"major": major, "info": task_major}


@router.get("/select_enrollment_year")
async def select_enrollment_year(
        enrollment_year: Annotated[SSelectEnrollmentYear, Depends()]
):
    task_enrollment_year = await Repo.select_enrollment_year(enrollment_year)
    result = ''
    for row in task_enrollment_year:
        result = row[0], row[1], ': age at admission: ', int(row[3]) - int(row[2][:4]), 'course:', row[4]
    return {"enrollment_year": enrollment_year, "info": task_enrollment_year, "result": result}


@router.get("/select_status/{status}")
async def select_status(
        status: Annotated[SSelectStatus, Depends()]
):
    task_status = await Repo.select_status(status)
    return {"status": status, "info": task_status}


@router.delete("/delete_id/{id}")
async def delete_id(
        ssid: Annotated[SDeletePerson, Depends()]
):
    task_ssid = await Repo.delete_person(ssid)
    return {"delete_id": ssid, "info": task_ssid}


@router.put('/update_person/{id}/{name}/{full_name}')
async def update_person(
        ssid: Annotated[SUpdatePerson, Depends()]
):
    task_status = await Repo.update_person(ssid)
    return {"status": ssid, "info": task_status}

