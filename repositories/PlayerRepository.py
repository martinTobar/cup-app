# repositories/user_repository.py
from sqlalchemy.orm import Session
from models.Player import Player
from schemas.Player import Player as PlayerCreate


class PlayerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, email: str) -> Player | None:
        return self.db.query(Player).filter(Player.id == id).first()

    def create(self, player: PlayerCreate) -> PlayerCreate:
        db_player = Player(
            name=player.name,
            last_name=player.last_name,
            dob=player.dob,
            position=player.position,
            team=player.team,
        )
        self.db.add(db_player)

        self.db.commit()
        self.db.refresh(db_player)

        return db_player
