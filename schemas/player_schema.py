from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class PlayerCreate(BaseModel):
    name: str
    last_name: str
    dob: datetime
    position: str
    team_id: UUID
    team_name: str


class PlayerResponse(BaseModel):
    id: UUID
    name: str
    last_name: str
    dob: datetime
    position: str
    team_id: UUID
    team_name: str

    class Config:
        from_attributes = True
