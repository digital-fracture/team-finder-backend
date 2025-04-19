from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.model.user import User, UserReadBare


class _TeamIdsTable(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id", index=True)


class _TeamIdsRead(SQLModel):
    id: int


class _TeamBase(SQLModel):
    name: str
    description: str = Field(default="")
    university: str | None = Field(default=None)
    event: str | None = Field(default=None)


class Team(_TeamBase, _TeamIdsTable, table=True):
    owner: "User" = Relationship()
    # members: list["User"] = Relationship()  # TODO


class TeamCreate(_TeamBase):
    pass


class TeamUpdate(SQLModel):
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)
    university: str | None = Field(default=None)
    event: str | None = Field(default=None)


class TeamReadBare(_TeamBase, _TeamIdsRead):
    pass


class TeamRead(TeamReadBare):
    owner: "UserReadBare"
    members: list["UserReadBare"]
