from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TeamCreate(BaseModel):
    name: str
    foundation_date: datetime


class TeamResponse(BaseModel):
    id: UUID
    name: str
    foundation_date: datetime

    class Config:
        from_attributes = True
