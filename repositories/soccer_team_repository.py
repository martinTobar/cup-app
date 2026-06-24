from sqlalchemy.orm import Session
from models.team import Team
from schemas.team_schema import TeamCreate
from uuid import uuid4

from .generic_repository import GenericRepository


class SoccerTeamRepository(GenericRepository):
    def __init__(self, db: Session):
        self.db = db
        self.class_Type = Team

    def create(self, team: TeamCreate) -> Team:
        db_team = Team(
            id=uuid4(),
            name=team.name,
            foundation_date=team.foundation_date,
        )
        self.db.add(db_team)
        self.db.commit()
        self.db.refresh(db_team)
        return db_team
