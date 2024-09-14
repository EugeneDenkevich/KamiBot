"""init

Revision ID: c5ddcde764e2
Revises:
Create Date: 2024-09-14 22:55:08.633250

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c5ddcde764e2"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "dialogs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("topic", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("dialogs")
    # ### end Alembic commands ###
