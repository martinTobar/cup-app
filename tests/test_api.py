import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

import models  # noqa: F401 — registers Team and Player in SQLModel.metadata
from core import database as db
from main import app

SQLITE_URL = "sqlite:///:memory:"

POSITION_MAP = {
    "Goalkeeper": "ARQ",
    "Defender": "DEF",
    "Midfielder": "MED",
    "Forward": "DEL",
}

ARGENTINA_TEAM = {
    "name": "Argentina",
    "foundation_date": "1893-02-27T00:00:00",
}

SAMPLE_PLAYERS = [
    {
        "name": "Lionel",
        "last_name": "Messi",
        "position": "DEL",
        "dob": "1987-06-24T00:00:00",
        "number": 10,
    },
    {
        "name": "Emiliano",
        "last_name": "Martínez",
        "position": "ARQ",
        "dob": "1992-09-02T00:00:00",
        "number": 23,
    },
    {
        "name": "Cristian",
        "last_name": "Romero",
        "position": "DEF",
        "dob": "1998-04-27T00:00:00",
        "number": 6,
    },
    {
        "name": "Leandro",
        "last_name": "Paredes",
        "position": "MED",
        "dob": "1994-06-29T00:00:00",
        "number": 5,
    },
]


@pytest.fixture(scope="module")
def client():
    engine = create_engine(
        SQLITE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    def override_get_db():
        yield session

    app.dependency_overrides[db.get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    session.close()
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def created_team(client):
    response = client.post("/team/", json=ARGENTINA_TEAM)
    assert response.status_code == 201
    return response.json()


@pytest.fixture(scope="module")
def created_players(client, created_team):
    players = []
    for p in SAMPLE_PLAYERS:
        payload = {
            **p,
            "team_id": created_team["id"],
            "team_name": created_team["name"],
        }
        response = client.post("/player/", json=payload)
        assert response.status_code == 201
        players.append(response.json())
    return players


class TestTeam:
    def test_create_team_returns_201(self, created_team):
        assert created_team["name"] == ARGENTINA_TEAM["name"]
        assert "id" in created_team

    def test_get_team_by_id(self, client, created_team):
        response = client.get(f"/team/{created_team['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == created_team["id"]
        assert data["name"] == "Argentina"

    def test_get_all_teams_includes_argentina(self, client, created_team):
        response = client.get("/team/")
        assert response.status_code == 200
        ids = [t["id"] for t in response.json()]
        assert created_team["id"] in ids

    def test_get_nonexistent_team_returns_404(self, client):
        response = client.get("/team/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404


class TestPlayer:
    def test_create_players_return_correct_fields(self, created_players):
        for player, expected in zip(created_players, SAMPLE_PLAYERS):
            assert player["name"] == expected["name"]
            assert player["last_name"] == expected["last_name"]
            assert player["position"] == expected["position"]
            assert player["number"] == expected["number"]
            assert "id" in player

    def test_get_player_by_id(self, client, created_players):
        messi = created_players[0]
        response = client.get(f"/player/{messi['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Lionel"
        assert data["last_name"] == "Messi"
        assert data["number"] == 10

    def test_player_has_correct_team(self, client, created_players, created_team):
        for player in created_players:
            response = client.get(f"/player/{player['id']}")
            assert response.status_code == 200
            assert response.json()["team_id"] == created_team["id"]

    def test_get_nonexistent_player_returns_404(self, client):
        response = client.get("/player/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404
