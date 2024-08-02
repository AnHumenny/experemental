from pydantic import BaseModel


class SUser(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class SUserInDB(SUser):
    hashed_password: str


