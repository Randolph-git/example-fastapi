"""add user table

Revision ID: dfb54e2d1b29
Revises: daf5ca6d5ba6
Create Date: 2023-11-08 14:53:58.097306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dfb54e2d1b29'
down_revision: Union[str, None] = 'daf5ca6d5ba6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False), 
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'))
    
    pass


def downgrade() -> None:
    op.drop_table('users') # drops users table from database.   
    pass
