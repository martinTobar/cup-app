This is a project and WIP I created to learn FastApi a couple months ago. Today Im using it to go again (as a recorderis and to update my knowledge) over the basics of deploying a web app to AWS by using good practices and industry standards. 

# Cup App

A FastAPI backend for managing soccer cup data (teams and players, with matches planned), backed by PostgreSQL via SQLModel/SQLAlchemy and Alembic migrations. It also ships a small React UI for manual testing, served by the same app.

## Tech stack

- **Python 3.13** managed with [uv](https://docs.astral.sh/uv/)
- **FastAPI** for the HTTP API
- **SQLModel / SQLAlchemy** for the ORM, **PostgreSQL** as the database
- **Alembic** for schema migrations
- **pytest** for tests, **ruff** for linting/formatting (wired as a pre-commit hook)
- **Docker / Docker Compose** for local containerized runs
- **Terraform** for AWS infrastructure (ECR, VPC, security groups)
- **FastMCP** to expose the data to AI agents as an [MCP](https://modelcontextprotocol.io) server

## Project structure

```
main.py                  # FastAPI app: route definitions only
mcp_server.py            # MCP server: exposes read-only tools to AI agents
core/database.py         # Engine/session setup from DATABASE_URL, get_db() dependency
models/                  # SQLModel table classes (Player, Team; Match is stubbed)
schemas/                 # Pydantic *Create (request) / *Response (response) models
repositories/            # One repository per entity, subclassing GenericRepository
alembic/                 # Migration environment and versions
frontend/                # Manual-test React UI (no build step), mounted at "/"
tests/                   # API tests using an in-memory SQLite database
terraform/               # AWS infrastructure: ECR, VPC/subnets, security groups
Dockerfile               # App image: runs migrations, then the server
compose.yaml             # web (app) + db (postgres:17) services
push_docker_img_to_ecr.sh# Build, tag and push the image to ECR
```

The app follows a layered structure: **routes (`main.py`) → repositories → SQLModel models**, with Pydantic schemas validating requests and serializing responses. Business logic lives in the repositories, not in route handlers.

## Getting started (local development)

1. Install dependencies (Python version is pinned in `.python-version`):

   ```sh
   uv sync
   ```

2. Create a `.env` file in the repo root. The app and Alembic both read `DATABASE_URL`; Docker Compose reads the `POSTGRES_*` variables:

   ```env
   DATABASE_URL=postgresql://<user>:<password>@localhost:5432/<db>
   POSTGRES_USER=<user>
   POSTGRES_PASSWORD=<password>
   POSTGRES_DB=<db>
   POSTGRES_PORT=5432
   ```

3. Apply migrations against your database:

   ```sh
   uv run alembic upgrade head
   ```

4. Run the dev server:

   ```sh
   uv run fastapi dev main.py
   ```

Then open:

- http://127.0.0.1:8000/ — manual-test UI (React, transpiled in the browser, no build step)
- http://127.0.0.1:8000/docs — interactive OpenAPI docs

## Running with Docker Compose

With the `POSTGRES_*` variables set in `.env`:

```sh
docker compose up --build
```

This starts a `postgres:17` container and the app container, which waits for the database to be healthy, applies Alembic migrations, and starts the server. The app is exposed at **http://localhost:5000** (container port 8000).

## API overview

| Method | Path                | Description                          |
| ------ | ------------------- | ------------------------------------ |
| GET    | `/player/positions` | List valid player positions          |
| GET    | `/player/{id}`      | Get a player by UUID                 |
| POST   | `/player/`          | Create a player                      |
| GET    | `/team/`            | List all teams                       |
| GET    | `/team/{id}`        | Get a team by UUID                   |
| POST   | `/team/`            | Create a team                        |
| GET    | `/health`           | Health check                         |

Player positions are constrained to `ARQ`, `DEF`, `MED`, `DEL` (defined once in `schemas/player_schema.py` and served to the UI via `GET /player/positions`).

## MCP server

`mcp_server.py` exposes the cup data to AI agents through the [Model Context Protocol](https://modelcontextprotocol.io), built with [FastMCP](https://gofastmcp.com). An MCP client (VS Code Copilot agent mode, Claude Desktop, Cursor, …) can discover these tools and call them to answer questions about the data in natural language.

The tools reuse the same repositories as the REST API, so the agent and HTTP clients get their data the same way.

| Tool           | Description                   |
| -------------- | ----------------------------- |
| `list_players` | List all players in the database |
| `list_teams`   | List all teams in the database   |

Both tools are read-only.

### Running it

```sh
uv run mcp_server.py
```

### Planned

- Serve MCP over HTTP from the FastAPI app itself (mounted at `/mcp`), so the deployed app exposes the REST API, the UI and the MCP endpoint from one container.
- A chat page where an agent answers questions using these tools, so the feature can be tried from the browser.

## Tests

Tests run against an in-memory SQLite database (no Postgres needed):

```sh
uv run pytest
```

## Linting and formatting

```sh
uv run ruff check --fix
uv run ruff format
```

Or run all pre-commit hooks:

```sh
uv run pre-commit run --all-files
```

## Migrations

Models in `models/` are the source of truth (`alembic/env.py` targets `SQLModel.metadata`). Any new or changed model must be imported in `models/__init__.py` for autogenerate to pick it up.

```sh
uv run alembic revision --autogenerate -m "description"
uv run alembic upgrade head
```

## Deployment (AWS)

The `terraform/` directory provisions the AWS infrastructure in `us-east-1`:

- **`ecr.tf`** — an ECR repository named `cup-app`, with image scanning on push.
- **`vpc.tf`** — a VPC (`10.0.0.0/16`) with two public and two private subnets spread across `us-east-1a`/`us-east-1b`, an internet gateway, and a public route table associated with the public subnets.
- **`security_groups.tf`** — security groups for the planned ALB → ECS → RDS architecture: the ALB accepts HTTP (port 80) from the internet, the ECS instances accept traffic on port 8000 only from the ALB, and the RDS Postgres database accepts traffic on port 5432 only from the ECS instances.

The ALB, ECS service, and RDS instance themselves are not defined yet — only the network and security groups they will use.

To apply:

```sh
cd terraform
terraform init
terraform apply
```

Then build and push the image (requires the AWS CLI to be configured):

```sh
./push_docker_img_to_ecr.sh
```

## Adding a new entity

Follow the existing pattern:

1. Add a SQLModel class in `models/` and export it from `models/__init__.py`.
2. Add `*Create` / `*Response` schemas in `schemas/`.
3. Add a repository subclassing `GenericRepository` in `repositories/` and export it from `repositories/__init__.py`.
4. Wire up routes in `main.py`.
5. Generate and apply an Alembic migration.
