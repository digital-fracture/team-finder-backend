__all__ = ["main"]

import logfire
import uvicorn

from .api import app
from .core.config import LOGFIRE_ENVIRONMENT, LOGFIRE_SERVICE_NAME


def main() -> None:
    logfire.configure(
        service_name=LOGFIRE_SERVICE_NAME,
        environment=LOGFIRE_ENVIRONMENT,
        send_to_logfire="if-token-present",
    )

    logfire.instrument_pydantic()
    logfire.instrument_fastapi(app)

    uvicorn.run(
        app,
        host="0.0.0.0",  # noqa: S104
        port=8000,
    )
