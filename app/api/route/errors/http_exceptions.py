__all__ = [
    "invalid_credentials",
    "invalid_token",
    "session_expired",
    "user_email_conflict",
    "user_not_found",
]

from fastapi import HTTPException, status

from . import messages

invalid_credentials = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.INVALID_CREDENTIALS)
invalid_token = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.INVALID_TOKEN)
session_expired = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.SESSION_EXPIRED)
user_email_conflict = HTTPException(status_code=status.HTTP_409_CONFLICT, detail=messages.USER_EMAIL_CONFLICT)
user_not_found = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND)
