from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel

# Single source of truth for valid positions: drives both validation here
# and the UI dropdown, which fetches this list via GET /player/positions
# (see main.py) instead of hardcoding it.
PLAYER_POSITIONS = ("ARQ", "DEF", "MED", "DEL")
PlayerPosition = Literal[PLAYER_POSITIONS]


class PlayerCreate(BaseModel):
    name: str
    last_name: str
    dob: datetime
    position: PlayerPosition
    number: int
    team_id: UUID
    team_name: str


class PlayerResponse(BaseModel):
    id: UUID
    name: str
    last_name: str
    dob: datetime
    position: PlayerPosition
    number: int
    team_id: UUID
    team_name: str

    class Config:
        from_attributes = True
