from sqlmodel import Field, SQLModel


class TeamInviteLink(SQLModel, table=True):
    __tablename__ = "_link_team_invite"

    team_id: int = Field(foreign_key="team.id", ondelete="CASCADE", primary_key=True)
    user_id: int = Field(foreign_key="user.id", ondelete="CASCADE", primary_key=True)
