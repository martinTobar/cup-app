from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette import status
from uuid import UUID

from core import database as db
from repositories import PlayerRepository, SoccerTeamRepository
from schemas.player_schema import PLAYER_POSITIONS, PlayerCreate, PlayerResponse
from schemas.team_schema import TeamCreate, TeamResponse

FRONTEND_DIR = Path(__file__).parent / "frontend"


@asynccontextmanager
async def on_startup(app: FastAPI):
    yield


app = FastAPI(lifespan=on_startup)

# Kept for flexibility (e.g. pointing the UI's "API base URL" field at this
# server from a different origin); not required for the setup below, where
# the UI is served from this same app.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/player/positions", response_model=list[str])
async def read_player_positions():
    return PLAYER_POSITIONS


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


@app.get("/team/", response_model=list[TeamResponse])
async def read_teams(session: Session = Depends(db.get_db)):
    repo = SoccerTeamRepository(session)
    return repo.get_all()


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


# Serves the manual-test UI (frontend/index.html) at "/" and its assets
# (app.jsx, styles.css) alongside it. Mounted last so it only catches
# requests that don't match an API route above.
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
