from typing import Annotated

import aiobcrypt
from fastapi import APIRouter, Body, HTTPException, status
from sqlmodel import select

from app.model import User, UserCreate, UserReadFull

from ..dependencies import AuthUser, DatabaseSession

user_router = APIRouter(tags=["user"])


@user_router.get(
    "/user",
    response_model=UserReadFull,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"detail": "Invalid token"},
        status.HTTP_401_UNAUTHORIZED: {"detail": "Session expired"},
        status.HTTP_404_NOT_FOUND: {"detail": "User not found"},
    },
)
async def get_user(user: AuthUser) -> ...:
    return user


@user_router.get(
    "/user/{user_id}",
    response_model=UserReadFull,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"detail": "User not found"},
    },
)
async def get_user_by_id(user_id: int, session: DatabaseSession) -> ...:
    statement = select(User).where(User.id == user_id)
    user: User | None = (await session.exec(statement)).one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


@user_router.post(
    "/user",
    response_model=UserReadFull,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {"detail": "User with this email already exists"},
    },
)
async def create_user(user_create: Annotated[UserCreate, Body(embed=True)], session: DatabaseSession) -> ...:
    hashed_password = (await aiobcrypt.hashpw(user_create.password.encode(), await aiobcrypt.gensalt())).decode()
    extra_data = {"hashed_password": hashed_password}

    user = User.model_validate(user_create, update=extra_data)

    session.add(user)
    await session.flush()
    await session.refresh(user)

    return user


@user_router.patch(
    "/user",
    response_model=UserReadFull,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"detail": "Invalid token"},
        status.HTTP_401_UNAUTHORIZED: {"detail": "Session expired"},
        status.HTTP_404_NOT_FOUND: {"detail": "User not found"},
    },
)
async def update_user(
        user: AuthUser, user_update: Annotated[UserCreate, Body(embed=True)], session: DatabaseSession
) -> ...:
    user.sqlmodel_update(user_update.model_dump(exclude_unset=True))

    session.add(user)
    await session.flush()
    await session.refresh(user)

    return user


@user_router.delete(
    "/user",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_400_BAD_REQUEST: {"detail": "Invalid token"},
        status.HTTP_401_UNAUTHORIZED: {"detail": "Session expired"},
        status.HTTP_404_NOT_FOUND: {"detail": "User not found"},
    },
)
async def delete_user(user: AuthUser, session: DatabaseSession) -> ...:
    session.delete(user)
    await session.flush()
