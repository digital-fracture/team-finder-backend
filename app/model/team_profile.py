from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .team import Team, TeamReadWithUsers


class _TeamProfileIdTable(SQLModel):
    team_id: int = Field(foreign_key="team.id", primary_key=True)


class _TeamProfileIdRead(SQLModel):
    team_id: int


class _TeamProfileBase(SQLModel):
    description: str = Field(default="")
    university: str | None = Field(default=None)
    event: str | None = Field(default=None)


class TeamProfile(_TeamProfileBase, _TeamProfileIdTable, table=True):
    __tablename__ = "team_profile"

    team: "Team" = Relationship(back_populates="profile")


class TeamProfileCreate(_TeamProfileBase):
    pass


class TeamProfileUpdate(SQLModel):
    description: str | None = None
    university: str | None = None
    event: str | None = None


class TeamProfileReadBare(_TeamProfileBase, _TeamProfileIdRead):
    pass


class TeamProfileReadFull(TeamProfileReadBare):
    team: "TeamReadWithUsers"
