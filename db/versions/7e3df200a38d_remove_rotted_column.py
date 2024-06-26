"""remove rotted column

Revision ID: 7e3df200a38d
Revises: c41abb284c8f
Create Date: 2021-10-20 17:16:08.299404

"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "7e3df200a38d"
down_revision = "c41abb284c8f"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("weblinks", "rotted")


def downgrade():
    op.add_column(
        "weblinks",
        sa.Column("rotted", sa.VARCHAR(), nullable=False, server_default="no"),
    )
