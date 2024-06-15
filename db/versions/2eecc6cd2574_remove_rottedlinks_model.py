"""Remove RottedLinks model

Revision ID: 2eecc6cd2574
Revises: bc15afca58dd
Create Date: 2024-06-15 18:09:03.582531

"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "2eecc6cd2574"
down_revision = "bc15afca58dd"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("rotted_links")


def downgrade():
    op.create_table(
        "rotted_links",
        sa.Column("id", sa.VARCHAR(), nullable=False),
        sa.Column("times_failed", sa.INTEGER(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
