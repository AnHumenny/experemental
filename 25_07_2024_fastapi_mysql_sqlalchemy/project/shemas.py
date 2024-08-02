from typing import Annotated
from pydantic import BaseModel
from fastapi import Path


class SProject(BaseModel):
    name: Annotated[str, Path(max_length=30)]
    location: Annotated[str, Path(max_length=250)]
    participants: Annotated[str, Path(max_length=250)]
    cost: Annotated[int, Path(ge=1, le=10000000)]


class SProjectId(BaseModel):
    id: int


class SProjectUpdate(SProject):
    id: int


class SProjectUpdateName(SProject):
    pass


class SProjectDelete(BaseModel):
    id: int
