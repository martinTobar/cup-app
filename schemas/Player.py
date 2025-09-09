from pydantic import BaseModel
from datetime import datetime


class Player(BaseModel):
    # id: int | None
    name: str
    last_name: str
    dob: datetime  # Date of Birth in YYYY-MM-DD format
    position: str
    team: str
    test: str | None = None

    class Config:
        from_attributes = True
