from pydantic import BaseModel
from typing import Annotated, Union
from fastapi import Path


class SPerson(BaseModel):
    name: Annotated[str, Path(max_length=15)]
    full_name: Annotated[str, Path(max_length=15)]
    date_of_birth: Annotated[str, Path(max_length=11)]
    phone: int
    enrollment_year: Union[str, None, Annotated[str, Path(max_length=11)]] = None
    course: Union[int, None, Annotated[int, Path(le=1)]] = None
    major: Union[str, None, Annotated[str, Path(max_length=30)]] = None
    status: Annotated[str, Path(max_length=20)]


class SSelectEnrollmentYear(BaseModel):
    enrollment_year: int


class SSelectCourse(BaseModel):
    course: Annotated[int, Path(le=5)]


class SSelectMajor(BaseModel):
    major: Annotated[str, Path(max_length=15)]


class SSelectStatus(BaseModel):
    status: Annotated[str, Path(max_length=15)]


class SUpdatePerson(BaseModel):
    id: int
    name: Annotated[str, Path(max_length=15)]


class SDeletePerson(BaseModel):
    id: int




