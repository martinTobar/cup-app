from sqlalchemy.orm import Session
from sqlmodel import SQLModel
from uuid import UUID


class GenericRepository:
    def __init__(self, db: Session):
        self.db = db
        self.class_Type = None

    def get_by_id(self, id: UUID) -> SQLModel | None:
        return self.db.query(self.class_Type).filter(self.class_Type.id == id).first()
