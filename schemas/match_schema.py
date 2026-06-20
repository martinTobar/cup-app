from pydantic import BaseModel
from datetime import datetime


class MatchSchema(BaseModel):
    "Class representing a pydantic soccer match entity"

    local_team: str
    visitor_team: str
    date: datetime  # Date of the match in YYYY-MM-DD format
    local_score: int
    visitor_score: int

    class Config:
        from_attributes = True
