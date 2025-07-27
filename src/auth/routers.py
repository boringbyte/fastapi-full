from datetime import timedelta
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserCreateModel, UserResponseModel, UserLoginModel
from .service import UserService
from .utils import create_access_token, decode_token, verify_password
from src.db.main import get_session
from fastapi.exceptions import HTTPException

auth_router = APIRouter()
user_service = UserService()
REFRESH_TOKEN_EXPIRY = 2

# Bearer Token

@auth_router.post("/signup", response_model=UserResponseModel,
                  status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exists = await user_service.user_exists(email, session=session)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User with email {email} already exists")
    new_user = await user_service.create_user(user_data, session)
    return new_user


@auth_router.post("/login")
async def login_user(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password
    user = await user_service.get_user_by_email(email, session=session)
    if user:
        valid_password = verify_password(password, user.password_hash)
        if valid_password:
            access_token = create_access_token(user_data={
                "email": user.email,
                "user_uid": str(user.uid)
            })
            refresh_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)},
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY))
            return JSONResponse(
                content={"message": "Login Successful", "access_token": access_token, "refresh_token": refresh_token,
                         "user": {"email": user.email, "uid": str(user.uid)}}
            )
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid email or password")
