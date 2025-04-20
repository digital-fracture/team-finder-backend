from datetime import UTC, datetime, timedelta

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from app.core.config import PRIVATE_KEY, PUBLIC_KEY
from app.core.exceptions import InvalidTokenError as CustomInvalidTokenError
from app.core.exceptions import TokenExpiredError


class TokenService:
    _jwt_algorithm = "RS256"

    @classmethod
    def generate_token(cls, user_id: int) -> str:
        """Generate ``access_token`` with the subject of ``user_id``"""
        now = datetime.now(UTC)

        payload = {"sub": str(user_id)}

        return jwt.encode(
            payload=payload | {"exp": now + timedelta(days=1)},
            key=PRIVATE_KEY,
            algorithm=cls._jwt_algorithm,
        )

    @classmethod
    def decode_token(cls, token: str) -> int:
        """Decode ``token`` and return ``user_id``"""
        try:
            payload = jwt.decode(
                jwt=token, key=PUBLIC_KEY, algorithms=(cls._jwt_algorithm,)
            )

            return int(payload["sub"])

        except ExpiredSignatureError as e:
            raise TokenExpiredError from e

        except (InvalidTokenError, ValueError) as e:
            raise CustomInvalidTokenError from e
