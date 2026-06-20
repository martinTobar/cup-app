from datetime import datetime
from sqlmodel import Field, SQLModel
from uuid import UUID


class Player(SQLModel, table=True):
    "Class representing a player entity"

    __tablename__ = "Player"

    id: UUID = Field(primary_key=True)
    name: str = Field(index=True)
    last_name: str
    dob: datetime  # Date of Birth in YYYY-MM-DD format
    position: str = Field(index=True)
    team_id: UUID = Field(foreign_key="Team.id")
    team_name: str = Field(index=True)
