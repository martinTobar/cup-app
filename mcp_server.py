from fastmcp import FastMCP
from repositories import PlayerRepository, SoccerTeamRepository
from core import database as db

mcp = FastMCP("cup-app")


@mcp.tool()
def list_players() -> list[str]:
    """List all the players in the database"""
    pr = PlayerRepository(next(db.get_db()))
    return [str(player) for player in pr.get_all()]


@mcp.tool()
def list_teams() -> list[str]:
    """List all the teams in the database"""
    tr = SoccerTeamRepository(next(db.get_db()))
    return [str(team) for team in tr.get_all()]


if __name__ == "__main__":
    mcp.run()
# This will not be executed when the module is imported,
# but will be executed when the module is run directly.
# Use `uv run python mcp_server.py` to start the FastMCP server.
