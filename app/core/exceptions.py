class AppError(Exception):
    pass


class UnexpectedError(AppError):
    pass


class TokenExpiredError(AppError):
    pass


class InvalidTokenError(AppError):
    pass
