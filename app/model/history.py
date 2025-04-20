from sqlmodel import Field, SQLModel


class HistoryUserLink(SQLModel, table=True):
    __tablename__ = "_link_history_user"

    user_id: int = Field(foreign_key="user.id", ondelete="CASCADE", primary_key=True)
    viewed_id: int = Field(foreign_key="user.id", ondelete="CASCADE", primary_key=True)


class HistoryTeamLink(SQLModel, table=True):
    __tablename__ = "_link_history_team"

    user_id: int = Field(foreign_key="user.id", ondelete="CASCADE", primary_key=True)
    viewed_id: int = Field(foreign_key="team.id", ondelete="CASCADE", primary_key=True)
