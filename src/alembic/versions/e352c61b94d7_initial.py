"""Initial.

Revision ID: e352c61b94d7
Revises:
Create Date: 2022-01-20 01:21:02.520636
"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "e352c61b94d7"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "game",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("word", sa.String(length=10), nullable=False),
        sa.Column("attempts", sa.SmallInteger(), nullable=False),
        sa.Column("start_time", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_game_id"), "game", ["id"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_game_id"), table_name="game")
    op.drop_table("game")
