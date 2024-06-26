from typing import Annotated

from fastapi import Depends
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from config import user_router
from data.models import User
from data.schemas import UserModel, TokenModel
from resource.auth import get_password_hash, create_access_token, verify_password, CurrentUser


@user_router.post("/signup")
async def signup_user(userdata: UserModel.UserCreateModel):
    user_exists = await User.exists(username=userdata.username.lower())
    if not user_exists:
        await User.create(
            username=userdata.username,
            fullname=userdata.fullname,
            password=get_password_hash(
                userdata.password
            )
        )
        raise HTTPException(201, 'User created successfully.')
    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="User already exists")


@user_router.post("/login")
async def login_user(userdata: Annotated[OAuth2PasswordRequestForm, Depends()], ) -> TokenModel:
    user = await User.get_or_none(username=userdata.username.lower())
    if user and verify_password(userdata.password, user.password):
        access_token = create_access_token({'sub': userdata.username})
        return access_token
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")


@user_router.get('/check-auth')
async def checking_authorized(user: CurrentUser):
    return {'ok': True}
