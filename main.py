from typing import Union

from fastapi import FastAPI, Depends
from models.Player import Player
from schemas.Player import Player as player_schema
from core import database as db

from contextlib import asynccontextmanager

from sqlalchemy.orm import Session

from repositories.PlayerRepository import PlayerRepository

from starlette import status


@asynccontextmanager
async def on_startup(app: FastAPI):
    db.get_db()
    print("helllo")
    yield


app = FastAPI(lifespan=on_startup)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/player/{player_id}")
async def read_player(player_id: int):
    # Dummy data for demonstration; in a real application, fetch from a database
    dummy_player = Player(
        id=1,
        name="Juan",
        last_name="Doe",
        dob="1990-01-01",
        position="Forward",
        team="Dream Team",
    )
    return {"player_id": player_id, "player": dummy_player}


@app.post("/player/", status_code=status.HTTP_201_CREATED, response_model=player_schema)
def create_player(player: player_schema, db: Session = Depends(db.get_db)):
    repo = PlayerRepository(db)
    return repo.create(player)
