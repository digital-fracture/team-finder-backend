from sqlmodel import Field, Relationship, SQLModel

from .user_profile import UserProfile, UserProfileReadBare
from .user_skill import UserSkill, UserSkillRead


class _UserIdTable(SQLModel):
    id: int | None = Field(default=None, primary_key=True)


class _UserEmail(SQLModel):
    email: str = Field(index=True)


class _UserPasswordHash(SQLModel):
    password_hash: str


class _UserRawPassword(SQLModel):
    password: str


class _UserIdRead(SQLModel):
    id: int


class _UserBase(SQLModel):
    username: str = Field(index=True)
    description: str
    photo_url: str | None = Field(default=None)

    telegram_username: str | None = Field(default=None)

    is_premium: bool = Field(default=False)
    collect_telemetry: bool = Field(default=True)


class User(_UserBase, _UserPasswordHash, _UserEmail, _UserIdTable, table=True):
    __tablename__ = "user"

    average_skill_level: float = Field(default=0)  # just for search sorting

    skills: list[UserSkill] = Relationship(back_populates="user")
    profile: UserProfile | None = Relationship(back_populates="user")


class UserCreate(_UserBase, _UserRawPassword, _UserEmail, _UserIdTable):
    pass


class UserUpdate(SQLModel):
    description: str | None = None
    photo_url: str | None = None
    telegram_username: str | None = None
    is_premium: bool | None = None
    collect_telemetry: bool | None = None


class UserReadBare(_UserBase, _UserEmail, _UserIdRead):
    skills: list[UserSkillRead] = []


class UserRead(UserReadBare):
    profile: UserProfileReadBare | None = None
