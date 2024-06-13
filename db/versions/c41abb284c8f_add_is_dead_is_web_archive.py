"""add is_dead, is_web_archive columns

Revision ID: c41abb284c8f
Revises:
Create Date: 2021-10-20 16:38:27.128115

"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "c41abb284c8f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "weblinks",
        sa.Column("is_dead", sa.Integer(), server_default="0", nullable=False),
    )
    op.add_column(
        "weblinks",
        sa.Column("is_web_archive", sa.Integer(), server_default="0", nullable=False),
    )


def downgrade():
    op.drop_column("weblinks", "is_web_archive")
    op.drop_column("weblinks", "is_dead")
