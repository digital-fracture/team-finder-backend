from sqlmodel import Field, SQLModel


class TeamRequestLink(SQLModel, table=True):
    __tablename__ = "_link_team_request"

    user_id: int = Field(foreign_key="user.id", ondelete="CASCADE", primary_key=True)
    team_id: int = Field(foreign_key="team.id", ondelete="CASCADE", primary_key=True)
