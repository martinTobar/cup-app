from sqlalchemy.orm import Session
from models.player import Player
from schemas.player_schema import PlayerCreate
from uuid import uuid4

from .generic_repository import GenericRepository


class PlayerRepository(GenericRepository):
    def __init__(self, db: Session):
        self.db = db
        self.class_Type = Player

    def create(self, player: PlayerCreate) -> Player:
        db_player = Player(
            id=uuid4(),
            name=player.name,
            last_name=player.last_name,
            dob=player.dob,
            position=player.position,
            team_id=player.team_id,
            team_name=player.team_name,
        )
        self.db.add(db_player)
        self.db.commit()
        self.db.refresh(db_player)
        return db_player
