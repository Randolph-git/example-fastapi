"""add foreign key to posts table

Revision ID: f48bb414e768
Revises: dfb54e2d1b29
Create Date: 2023-11-08 16:02:46.261053

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f48bb414e768'
down_revision: Union[str, None] = 'dfb54e2d1b29'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE') 
    # op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False)) # adds owner_id column to posts table
    # ondelete='CASCADE' means that if the owner_id is deleted, the post will also be deleted.
    # source_table='posts' means that the foreign key will be on the posts table.
    # referent_table='users' means that the foreign key will be on the users table.
    # local_cols=['owner_id'] means that the foreign key will be on the owner_id column of the posts table.
    # remote_cols=['id'] means that the foreign key will be on the id column of the users table.
    # ondelete='CASCADE' means that if the owner_id is deleted, the post will also be deleted.
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts') # drops post_users_fk constraint from posts table.
    op.drop_column('posts', 'owner_id') # op.drop_column('posts', 'owner_id') # drops owner_id column from posts table.
    pass
