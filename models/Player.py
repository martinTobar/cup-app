from datetime import datetime
from sqlmodel import Field, SQLModel


class Player(SQLModel, table=True):
    __tablename__ = "Player"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    last_name: str
    dob: datetime  # Date of Birth in YYYY-MM-DD format
    position: str = Field(index=True)
    team: str = Field(index=True)
    test: str = Field(default=None, nullable=True)
