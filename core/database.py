from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
import os
from dotenv import load_dotenv
# from app.core.config import settings

load_dotenv()
SQLALCHEMY_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
myBase = SQLModel
print(myBase.metadata)
myBase.metadata.create_all(bind=engine)

print("Database connected")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
