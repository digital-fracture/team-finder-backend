__all__ = ["token_auth"]

from fastapi import status

from .models import (
    invalid_token_response,
    session_expired_response,
    user_not_found_response,
)

token_auth = {
    status.HTTP_400_BAD_REQUEST: invalid_token_response,
    status.HTTP_401_UNAUTHORIZED: session_expired_response,
    status.HTTP_404_NOT_FOUND: user_not_found_response,
}
