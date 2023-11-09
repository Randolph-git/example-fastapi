"""create posts table

Revision ID: edd29dadcaba
Revises: 
Create Date: 2023-11-08 14:22:37.618361

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# CREATE THIS FILE BY USING COMMAND: alembic revision -m "create posts table". the file is put in version folder

# revision identifiers, used by Alembic.
revision: str = 'edd29dadcaba'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# tracks updating table
def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('title', sa.String(), nullable=False)) # nullable=false means that the column cannot be null.
                    #primary key means that the column is the primary key.  primary key is unique.  primary key is the only thing that can be null.  
                    # primary key is the only thing that can be duplicated.  primary key is the only thing that can be updated.  primary key is the only thing that can be deleted.  primary key is the only thing that can be inserted.  primary key is the only thing that can be queried.  primary key is the only thing that can be queried.  primary key is the only thing that can be queried.  primary key is the only thing that can be queried.  primary key is the only thing that can be queried.  primary key is the only thing that can be queried.  primary key is the only thing that can be queried.  primary key is the only thing that can be queried.  primary key is the only thing that can be queried.  primary key is the only thing that can be queried.  primary key is
    pass

# tracks reverting table
def downgrade() -> None:
    op.drop_table('posts') # drops posts table from database.   
    pass
