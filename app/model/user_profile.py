from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User, UserReadBare


class _UserProfileIdTable(SQLModel):
    user_id: int = Field(foreign_key="user.id", ondelete="CASCADE", primary_key=True)


class _UserProfileIdRead(SQLModel):
    user_id: int


class _UserProfileBase(SQLModel):
    description: str = Field(default="")
    university: str | None = Field(default=None)


class UserProfile(_UserProfileBase, _UserProfileIdTable, table=True):
    __tablename__ = "user_profile"

    user: "User" = Relationship(
        back_populates="profile", sa_relationship_kwargs={"lazy": "selectin"}
    )


class UserProfileCreate(_UserProfileBase):
    pass


class UserProfileUpdate(SQLModel):
    description: str | None = None
    university: str | None = None


class UserProfileReadBare(_UserProfileBase, _UserProfileIdRead):
    pass


class UserProfileReadFull(UserProfileReadBare):
    user: "UserReadBare"
