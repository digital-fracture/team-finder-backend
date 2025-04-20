from sqlmodel import Field, Relationship, SQLModel

from .favourite import FavouriteTeamLink, FavouriteUserLink
from .history import HistoryTeamLink, HistoryUserLink
from .team import Team, TeamMemberLink, TeamReadId
from .team_invite import TeamInviteLink
from .team_request import TeamRequestLink
from .user_profile import UserProfile, UserProfileReadBare
from .user_skill import UserSkill, UserSkillRead


class _UserIdTable(SQLModel):
    id: int | None = Field(default=None, primary_key=True)


class _UserEmail(SQLModel):
    email: str = Field(unique=True, index=True)


class _UserPasswordHash(SQLModel):
    password_hash: str


class _UserRawPassword(SQLModel):
    password: str


class _UserIdRead(SQLModel):
    id: int


class _UserBase(SQLModel):
    username: str = Field(index=True)

    telegram_username: str | None = Field(default=None)

    is_premium: bool = Field(default=False)
    collect_telemetry: bool = Field(default=True)


class User(_UserBase, _UserPasswordHash, _UserEmail, _UserIdTable, table=True):
    __tablename__ = "user"

    average_skill_level: float = Field(default=0)  # just for search sorting

    skills: list[UserSkill] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    profile: UserProfile | None = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    teams: list[Team] = Relationship(
        back_populates="members",
        link_model=TeamMemberLink,
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    invites: list[Team] = Relationship(
        back_populates="invites",
        link_model=TeamInviteLink,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    requests: list[Team] = Relationship(
        back_populates="requests",
        link_model=TeamRequestLink,
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    favourite_users: list["User"] = Relationship(
        link_model=FavouriteUserLink,
        sa_relationship_kwargs={
            "primaryjoin": "User.id == FavouriteUserLink.user_id",
            "secondaryjoin": "User.id == FavouriteUserLink.favourite_id",
        },
    )
    favourite_teams: list[Team] = Relationship(link_model=FavouriteTeamLink)

    history_users: list["User"] = Relationship(
        link_model=HistoryUserLink,
        sa_relationship_kwargs={
            "primaryjoin": "User.id == HistoryUserLink.user_id",
            "secondaryjoin": "User.id == HistoryUserLink.viewed_id",
        },
    )
    history_teams: list[Team] = Relationship(link_model=HistoryTeamLink)


class UserCreate(_UserBase, _UserRawPassword, _UserEmail):
    pass


class UserUpdate(SQLModel):
    username: str | None = None
    description: str | None = None
    telegram_username: str | None = None
    is_premium: bool | None = None
    collect_telemetry: bool | None = None


class UserReadBare(_UserBase, _UserEmail, _UserIdRead):
    skills: list[UserSkillRead] = []


class UserReadWithProfile(UserReadBare):
    profile: UserProfileReadBare | None = None


class UserReadWithTeams(UserReadBare):
    teams: list[TeamReadId] = []


class UserReadFull(UserReadWithTeams, UserReadWithProfile):
    invites: list[TeamReadId] = []
    requests: list[TeamReadId] = []
