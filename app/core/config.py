import os

from sqlalchemy import URL

POSTGRES_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB"),
)

LOGFIRE_SERVICE_NAME = os.getenv("LOGFIRE_SERVICE_NAME")
LOGFIRE_ENVIRONMENT = os.getenv("LOGFIRE_ENVIRONMENT")

ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS", default="*").split(",")
