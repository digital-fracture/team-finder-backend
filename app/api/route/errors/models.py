__all__ = [
    "invalid_credentials_response",
    "invalid_token_response",
    "session_expired_response",
    "user_email_conflict_response",
    "user_not_found_response",
]

from pydantic import BaseModel

from . import messages


class _InvalidCredentialsError(BaseModel):
    detail: str = messages.INVALID_CREDENTIALS


class _InvalidTokenError(BaseModel):
    detail: str = messages.INVALID_TOKEN


class _SessionExpiredError(BaseModel):
    detail: str = messages.SESSION_EXPIRED


class _UserEmailConflictError(BaseModel):
    detail: str = messages.USER_EMAIL_CONFLICT


class _UserNotFoundError(BaseModel):
    detail: str = messages.USER_NOT_FOUND


invalid_credentials_response = {"model": _InvalidCredentialsError}
invalid_token_response = {"model": _InvalidTokenError}
session_expired_response = {"model": _SessionExpiredError}
user_email_conflict_response = {"model": _UserEmailConflictError}
user_not_found_response = {"model": _UserNotFoundError}
