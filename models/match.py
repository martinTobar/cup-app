# from datetime import datetime
# from sqlmodel import Field, SQLModel
# from uuid import UUID

# class Match(SQLModel, table=True):
#     "Class representing a soccer match entity"
#     __tablename__ = "Matches"

#     id: UUID | None = Field(default=None, primary_key=True)
#     local_team: str = Field(index=True, unique=True)
#     visitor_team: str
#     date: datetime  # Date of the match in YYYY-MM-DD format
#     local_score : int
#     visitor_score : int

