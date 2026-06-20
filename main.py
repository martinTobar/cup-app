from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from uuid import UUID

from core import database as db
from repositories import PlayerRepository, SoccerTeamRepository
from schemas.player_schema import PlayerCreate, PlayerResponse
from schemas.team_schema import TeamCreate, TeamResponse


@asynccontextmanager
async def on_startup(app: FastAPI):
    yield


app = FastAPI(lifespan=on_startup)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/player/{player_id}", response_model=PlayerResponse)
async def read_player(player_id: UUID, session: Session = Depends(db.get_db)):
    repo = PlayerRepository(session)
    player = repo.get_by_id(player_id)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Player not found"
        )
    return player


@app.post(
    "/player/", status_code=status.HTTP_201_CREATED, response_model=PlayerResponse
)
def create_player(player: PlayerCreate, session: Session = Depends(db.get_db)):
    repo = PlayerRepository(session)
    return repo.create(player)


@app.get("/team/{team_id}", response_model=TeamResponse)
async def read_team(team_id: UUID, session: Session = Depends(db.get_db)):
    repo = SoccerTeamRepository(session)
    team = repo.get_by_id(team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )
    return team


@app.post("/team/", status_code=status.HTTP_201_CREATED, response_model=TeamResponse)
def create_team(team: TeamCreate, session: Session = Depends(db.get_db)):
    repo = SoccerTeamRepository(session)
    return repo.create(team)
