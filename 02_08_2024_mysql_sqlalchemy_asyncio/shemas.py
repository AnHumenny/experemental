from pydantic import BaseModel


class SModelUser(BaseModel):
    name: str
    full_name: str
    age: int


class SModelUserId(SModelUser):
    id: int


class SModelCountry(BaseModel):
    map: str
    location: str
    name: str


class SModelCountryId(SModelCountry):
    id: int


