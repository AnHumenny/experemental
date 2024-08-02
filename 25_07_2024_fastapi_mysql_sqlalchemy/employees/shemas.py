from typing import Annotated
from pydantic import BaseModel, EmailStr
from fastapi import Path


class SEmployees(BaseModel):
    name: Annotated[str, Path(max_length=30)]
    phone: int      #!допилить по ограничению числа водимых символов!
    email: EmailStr
    area_of_responsibility: Annotated[str, Path(max_length=250)]
    post: Annotated[str, Path(max_length=30)]
    category: Annotated[int, Path(le=6)]


class SEmployeesId(BaseModel):
    id: Annotated[int, Path(le=1000)]


class SDeleteUser(BaseModel):
    id: int


class SUpdateSEmployeesId(SEmployees):
    id: int
