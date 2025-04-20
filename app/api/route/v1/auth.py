from fastapi import APIRouter, status

from ..dependencies import AuthToken, TokenSchema

auth_router = APIRouter(tags=["user"])


@auth_router.post(
    "/auth",
    response_model=TokenSchema,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_401_UNAUTHORIZED: {"detail": "Invalid credentials"}},
)
async def auth(token: AuthToken) -> ...:
    return token
