from sqlmodel import Field, SQLModel


class FavouriteUserLink(SQLModel, table=True):
    __tablename__ = "_link_favourite_user"

    user_id: int = Field(foreign_key="user.id", ondelete="CASCADE", primary_key=True)
    favourite_id: int = Field(
        foreign_key="user.id", ondelete="CASCADE", primary_key=True
    )


class FavouriteTeamLink(SQLModel, table=True):
    __tablename__ = "_link_favourite_team"

    user_id: int = Field(foreign_key="user.id", ondelete="CASCADE", primary_key=True)
    favourite_id: int = Field(
        foreign_key="team.id", ondelete="CASCADE", primary_key=True
    )
