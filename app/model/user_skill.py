from datetime import UTC, datetime
from enum import IntEnum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User


def _current_time_factory() -> datetime:
    return datetime.now(UTC)


class SkillLevel(IntEnum):
    ZERO = 0
    BEGINNER = 1
    MEDIUM = 2
    ADVANCED = 3


class _UserSkillIdsTable(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", ondelete="CASCADE", index=True)


class _UserSkillIdsRead(SQLModel):
    id: int


class _UserSkillBase(SQLModel):
    name: str = Field(index=True)
    level: SkillLevel
    confirmed_at: datetime = Field(default_factory=_current_time_factory)


class UserSkill(_UserSkillBase, _UserSkillIdsTable, table=True):
    __tablename__ = "user_skill"

    user: "User" = Relationship(
        back_populates="skills", sa_relationship_kwargs={"lazy": "selectin"}
    )


class UserSkillCreate(_UserSkillBase):
    pass


class UserSkillUpdate(SQLModel):
    level: SkillLevel | None = Field(default=None)
    confirmed_at: datetime = Field(default_factory=_current_time_factory)


class UserSkillRead(_UserSkillBase, _UserSkillIdsRead):
    pass
