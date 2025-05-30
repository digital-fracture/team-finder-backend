from typing import Annotated

import aiobcrypt
from fastapi import APIRouter, Body, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from app.model import User, UserCreate, UserReadFull, UserUpdate

from ..dependencies import AuthUser, DatabaseSession
from ..errors import http_exceptions, models, responses_presets

user_router = APIRouter(tags=["user"])


@user_router.get(
    "/user",
    response_model=UserReadFull,
    status_code=status.HTTP_200_OK,
    responses=responses_presets.token_auth,
)
async def get_user(user: AuthUser) -> ...:
    return user


@user_router.get(
    "/user/{user_id}",
    response_model=UserReadFull,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: models.user_not_found_response},
)
async def get_user_by_id(user_id: int, session: DatabaseSession) -> ...:
    statement = select(User).where(User.id == user_id)
    user: User | None = (await session.exec(statement)).one_or_none()

    if not user:
        raise http_exceptions.user_not_found

    return user


@user_router.post(
    "/user",
    response_model=UserReadFull,
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_409_CONFLICT: models.user_email_conflict_response},
)
async def create_user(
    user_create: Annotated[UserCreate, Body(embed=False)], session: DatabaseSession
) -> ...:
    hashed_password = (
        await aiobcrypt.hashpw(user_create.password.encode(), await aiobcrypt.gensalt())
    ).decode()
    extra_data = {"hashed_password": hashed_password}

    user = User.model_validate(user_create, update=extra_data)

    session.add(user)
    try:
        await session.flush()
    except IntegrityError as e:
        raise http_exceptions.user_email_conflict from e

    await session.refresh(user)

    return user


@user_router.patch(
    "/user",
    response_model=UserReadFull,
    status_code=status.HTTP_200_OK,
    responses=responses_presets.token_auth,
)
async def update_user(
    user: AuthUser,
    user_update: Annotated[UserUpdate, Body(embed=False)],
    session: DatabaseSession,
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
    responses=responses_presets.token_auth,
)
async def delete_user(user: AuthUser, session: DatabaseSession) -> ...:
    session.delete(user)
    await session.flush()
