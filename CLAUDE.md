# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A FastAPI backend for managing soccer cup data (players, teams, matches), using SQLModel/SQLAlchemy for ORM and Alembic for migrations. Package management is via `uv`.

## Commands

This project uses `uv` (see `uv.lock`, `pyproject.toml`). Python version is pinned to 3.13 (`.python-version`).

- Install dependencies: `uv sync`
- Run the dev server: `uv run fastapi dev main.py`
- Lint/format (ruff, also wired as a pre-commit hook): `uv run ruff check --fix` and `uv run ruff format`
- Run pre-commit hooks manually: `uv run pre-commit run --all-files`
- Database migrations (Alembic):
  - Generate a new migration: `uv run alembic revision --autogenerate -m "description"`
  - Apply migrations: `uv run alembic upgrade head`
- `DATABASE_URL` must be set in `.env` (loaded via `python-dotenv`) for both the app (`core/database.py`) and Alembic (`alembic/env.py`) to connect to the database.

There is no test suite configured yet.

## Architecture

The app follows a layered structure: **FastAPI routes (`main.py`) → repositories → SQLModel models**, with Pydantic schemas used for request/response validation.

- `core/database.py` — creates the SQLAlchemy engine/session from `DATABASE_URL` and exposes `get_db()`, a generator-based dependency used by FastAPI route handlers via `Depends(db.get_db)`.
- `models/` — SQLModel table classes (`Player`, `Team`; `Match` is currently commented out/unused in `models/match.py`). These double as the Alembic migration source of truth: `alembic/env.py` sets `target_metadata = SQLModel.metadata`, so any new/changed model must be imported in `models/__init__.py` to be picked up by autogenerate.
- `repositories/` — one repository class per entity (`PlayerRepository`, `SoccerTeamRepository`), each subclassing `GenericRepository` (`repositories/generic_repository.py`), which provides a generic `get_by_id`. Repositories are instantiated per-request in route handlers with the injected `Session`, and each implements its own `create()`.
- `schemas/` — Pydantic models split into `*Create` (request body) and `*Response` (`from_attributes = True`, for serializing ORM objects) per entity.
- `main.py` — route definitions only; business logic lives in repositories, not in route handlers.

When adding a new entity, the pattern to follow is: add a SQLModel in `models/`, export it from `models/__init__.py`, add `*Create`/`*Response` schemas in `schemas/`, add a repository subclassing `GenericRepository` in `repositories/` (exported from `repositories/__init__.py`), then wire up routes in `main.py`, and generate an Alembic migration.
