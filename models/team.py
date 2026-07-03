from datetime import datetime
from sqlmodel import Field, SQLModel
from uuid import UUID


class Team(SQLModel, table=True):
    "Class representing a soccer team entity"

    __tablename__ = "Team"

    id: UUID | None = Field(primary_key=True)
    name: str = Field(index=True, unique=True)
    foundation_date: datetime  # Date of the foundation in YYYY-MM-DD format
