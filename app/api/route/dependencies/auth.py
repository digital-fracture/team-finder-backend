from typing import Annotated

import aiobcrypt
from fastapi import Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlmodel import select

from app.core.exceptions import InvalidTokenError, TokenExpiredError
from app.model import User
from app.service import TokenService

from .database import DatabaseSession


class LoginSchema(BaseModel):
    email: str
    password: str


class TokenSchema(BaseModel):
    access_token: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


async def login_for_access_token(
    login: Annotated[LoginSchema, Body(embed=True)], session: DatabaseSession
) -> TokenSchema:
    statement = select(User).where(User.email == login.email)
    user: User | None = (await session.exec(statement)).one_or_none()

    if not user or not await aiobcrypt.checkpw(
        login.password.encode(), user.password_hash.encode()
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = await TokenService.generate_token(user.id)

    return TokenSchema(access_token=access_token)


AuthToken = Annotated[TokenSchema, Depends(login_for_access_token)]


async def get_current_user_id(token: Annotated[str, Depends(oauth2_scheme)]) -> int:
    try:
        return await TokenService.decode_token(token)

    except TokenExpiredError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired") from e

    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token") from e


AuthUserId = Annotated[int, Depends(get_current_user_id)]


async def get_current_user(user_id: AuthUserId, session: DatabaseSession) -> User:
    statement = select(User).where(User.id == user_id)
    user: User | None = (await session.exec(statement)).one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


AuthUser = Annotated[User, Depends(get_current_user)]
