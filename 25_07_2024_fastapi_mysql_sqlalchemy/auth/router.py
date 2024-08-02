#где-то на просторах сети ))
from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth.shemas import SUser, SUserInDB


router = APIRouter(
    prefix="/users"
)

users_db = {
    "user_1": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashed1",
        "disabled": False,
    },
    "user_2": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashed2",
        "disabled": False,
    },
    "user_3": {
            "username": "admin",
            "full_name": "vasya Pupkin",
            "email": "pupkin@example.com",
            "hashed_password": "fakehashed3",
            "disabled": False,
    },
}


def hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        print('user_dict', user_dict)
        return SUserInDB(**user_dict)


def fake_decode_token(token):
    user = get_user(users_db, token)
    print('user', user)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[SUser, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[SUser, Depends(get_current_user)],
):
    return current_user

