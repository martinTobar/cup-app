"""align player columns with model

Revision ID: 20ff55ef9543
Revises: b9e8eb9aa9d9
Create Date: 2026-06-20 17:30:04.037538

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20ff55ef9543"
down_revision: Union[str, Sequence[str], None] = "b9e8eb9aa9d9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

FK_NAME = "fk_Player_team_id_Team"


def upgrade() -> None:
    """Upgrade schema."""
    # "Player" had drifted from models/player.py: it carried a stray
    # "team" (varchar) and "test" column instead of "team_id"/"team_name",
    # and had no "number" column. Table is empty, so this is a clean swap.
    op.drop_index(op.f("ix_Player_team"), table_name="Player")
    op.drop_column("Player", "team")
    op.drop_column("Player", "test")

    op.add_column("Player", sa.Column("number", sa.Integer(), nullable=False))
    op.add_column("Player", sa.Column("team_id", sa.Uuid(), nullable=False))
    op.add_column("Player", sa.Column("team_name", sa.String(), nullable=False))
    op.create_index(op.f("ix_Player_team_name"), "Player", ["team_name"], unique=False)
    op.create_foreign_key(FK_NAME, "Player", "Team", ["team_id"], ["id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(FK_NAME, "Player", type_="foreignkey")
    op.drop_index(op.f("ix_Player_team_name"), table_name="Player")
    op.drop_column("Player", "team_name")
    op.drop_column("Player", "team_id")
    op.drop_column("Player", "number")

    op.add_column("Player", sa.Column("test", sa.String(), nullable=True))
    op.add_column("Player", sa.Column("team", sa.String(), nullable=False))
    op.create_index(op.f("ix_Player_team"), "Player", ["team"], unique=False)
