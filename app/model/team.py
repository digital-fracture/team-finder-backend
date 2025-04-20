from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from .team_invite import TeamInviteLink
from .team_profile import TeamProfile, TeamProfileReadBare
from .team_request import TeamRequestLink

if TYPE_CHECKING:
    from .user import User, UserReadWithProfile


class TeamMemberLink(SQLModel, table=True):
    team_id: int = Field(foreign_key="team.id", primary_key=True)
    user_id: int = Field(foreign_key="user.id", primary_key=True)


class _TeamIdsTable(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id", index=True)


class _TeamBase(SQLModel):
    name: str


class Team(_TeamBase, _TeamIdsTable, table=True):
    __tablename__ = "team"

    owner: "User" = Relationship()
    members: list["User"] = Relationship(back_populates="teams", link_model=TeamMemberLink)
    profile: TeamProfile | None = Relationship(back_populates="team")

    invites: list["User"] = Relationship(back_populates="invites", link_model=TeamInviteLink)
    requests: list["User"] = Relationship(back_populates="requests", link_model=TeamRequestLink)


class TeamCreate(_TeamBase):
    pass


class TeamUpdate(SQLModel):
    name: str | None = None


class TeamReadId(SQLModel):
    id: int


class TeamReadBare(_TeamBase, TeamReadId):
    pass


class TeamReadWithProfile(TeamReadBare):
    profile: TeamProfileReadBare | None = None


class TeamReadWithUsers(TeamReadBare):
    owner: "UserReadWithProfile"
    members: list["UserReadWithProfile"] = []


class TeamReadFull(TeamReadWithUsers, TeamReadWithProfile):
    invites: list["UserReadWithProfile"] = []
    requests: list["UserReadWithProfile"] = []
