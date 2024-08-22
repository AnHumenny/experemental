from typing import Annotated
from pydantic import BaseModel
from fastapi import Path


class SStatDayTypeCurrent(BaseModel):
    type_current: Annotated[str, Path(max_length=3)]


class SStatDayCurrent(BaseModel):
    date: Annotated[str, Path(max_length=10)]
