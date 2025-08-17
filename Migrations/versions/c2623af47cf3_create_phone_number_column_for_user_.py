"""Create phone_number column for user table

Revision ID: c2623af47cf3
Revises: 
Create Date: 2025-08-17 14:14:36.594897

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2623af47cf3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.add_column('users', sa.Column("phone_number", sa.String(), nullable=True))
    
    
def downgrade() -> None:
    op.drop_column('users', 'phone_number')
