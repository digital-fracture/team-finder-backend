# team-finder-backend

API for a team finding application

### [Website]()


## Run by yourself

### Docker Compose (via `make`)

1. Clone the repository:
    ```shell
    git clone https://github.com/digital-fracture/codd-street-graph-backend.git
    cd cold-start-backend
    ```

2. Run:
    ```shell
    make       # production
    ```
    ```shell
    make dev   # development
    ```


## Stack

- [python 3.13](https://python.org/) - programming language
- [uv](https://docs.astral.sh/uv/) - dependency manager
- [FastAPI](https://fastapi.tiangolo.com/) - web server engine
- [SQLAlchemy](https://www.sqlalchemy.org/) & [SQLModel](https://sqlmodel.tiangolo.com/) - ORM
- [asyncpg](https://magicstack.github.io/asyncpg/current/) - database engine **[Postgresql]**
- [aiobcrypt](https://github.com/blokje/aiobcrypt) for asynchronous password hashing (with salt)
- [JWT](https://jwt.io/) for user session management
- [Pydantic Logfire](https://pydantic.dev/logfire/) - rich logging (using OpenTelemetry)
- [ruff](https://astral.sh/ruff/) - linter and formatter
- [Traefik](https://traefik.io/) - API gateway & SSL/TLS certificate management
- [Docker Compose](https://docs.docker.com/compose/) & [GNU Make](https://www.gnu.org/software/make/) - deployment tool
- And more
