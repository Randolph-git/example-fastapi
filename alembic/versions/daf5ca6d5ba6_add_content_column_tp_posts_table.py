"""add content column tp posts table

Revision ID: daf5ca6d5ba6
Revises: edd29dadcaba
Create Date: 2023-11-08 14:48:06.974684

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'daf5ca6d5ba6'
down_revision: Union[str, None] = 'edd29dadcaba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content') # drops content column from posts table.   
    pass
