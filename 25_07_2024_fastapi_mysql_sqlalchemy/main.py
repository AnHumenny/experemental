from auth.router import hash_password, users_db
from auth.router import router as auth_router
from project.router import router as project_router
from employees.router import router as employees_router
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import OAuth2PasswordRequestForm
from auth.shemas import SUserInDB


app = FastAPI()


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = users_db.get(form_data.username)
    print("user_dict", user_dict)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = SUserInDB(**user_dict)
    hashed_password = hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}


app.include_router(auth_router)
app.include_router(project_router)
app.include_router(employees_router)



