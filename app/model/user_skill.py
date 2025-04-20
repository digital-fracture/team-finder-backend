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


class _UserSkillIds(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)


class _UserSkillBase(SQLModel):
    name: str = Field(index=True)
    level: SkillLevel
    confirmed_at: datetime = Field(default_factory=_current_time_factory)


class UserSkill(_UserSkillBase, _UserSkillIds, table=True):
    __tablename__ = "user_skill"

    user: "User" = Relationship(back_populates="skills")


class UserSkillCreate(_UserSkillBase):
    pass


class UserSkillUpdate(SQLModel):
    level: SkillLevel
    confirmed_at: datetime = Field(default_factory=_current_time_factory)


class UserSkillRead(_UserSkillBase):
    pass
