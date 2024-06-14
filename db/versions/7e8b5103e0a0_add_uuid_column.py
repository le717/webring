"""Create an uuid column

Revision ID: 7e8b5103e0a0
Revises: 7e3df200a38d
Create Date: 2024-06-13 16:50:51.162708

"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "7e8b5103e0a0"
down_revision = "7e3df200a38d"
branch_labels = None
depends_on = None

bind = op.get_bind()
session = sa.orm.Session(bind=bind)


def upgrade():
    op.add_column(
        "weblinks",
        sa.Column("uuid", sa.VARCHAR(), server_default=""),
    )
    session.execute(sa.text("UPDATE weblinks SET uuid = id"))
    with op.batch_alter_table("weblinks") as batch_op:
        batch_op.alter_column(
            "uuid",
            existing_type=sa.VARCHAR(),
            type_=sa.VARCHAR(),
            nullable=False,
        )


def downgrade():
    session.execute(sa.text("UPDATE weblinks SET id = uuid"))
    op.drop_column("weblinks", "uuid")
