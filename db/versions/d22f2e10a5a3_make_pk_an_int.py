"""Convert weblinks.id into an AUTOINCREMENT ID

Revision ID: d22f2e10a5a3
Revises: 7e8b5103e0a0
Create Date: 2024-06-13 17:33:16.543961

"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "d22f2e10a5a3"
down_revision = "7e8b5103e0a0"
branch_labels = None
depends_on = None

bind = op.get_bind()
session = sa.orm.Session(bind=bind)


def upgrade():
    with op.batch_alter_table("weblinks") as batch_op:
        batch_op.alter_column(
            "id",
            existing_type=sa.VARCHAR(),
            type_=sa.Integer(),
            autoincrement=True,
        )
        batch_op.create_primary_key("pk", ["id"])

    # Fix a weird issue where the first record's ID is 0
    session.execute(sa.text("UPDATE weblinks SET id = 1 where id = 0"))


def downgrade():
    with op.batch_alter_table("weblinks") as batch_op:
        batch_op.alter_column(
            "id",
            existing_type=sa.Integer(),
            type_=sa.VARCHAR(),
            existing_nullable=False,
        )
        batch_op.create_primary_key("pk", ["id"])
