"""change columns in lang_test

Revision ID: 33fa25447107
Revises: a641da50afca
Create Date: 2024-10-05 07:54:07.810249

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "33fa25447107"
down_revision: Union[str, None] = "a641da50afca"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "lang_tests", "current_question",
        existing_type=postgresql.JSON(astext_type=sa.Text()),
        type_=sa.String(),
        existing_nullable=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "lang_tests", "current_question",
        existing_type=sa.String(),
        type_=postgresql.JSON(astext_type=sa.Text()),
        existing_nullable=True,
    )
    # ### end Alembic commands ###
