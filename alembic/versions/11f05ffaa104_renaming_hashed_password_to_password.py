"""renaming  hashed_password to password

Revision ID: 11f05ffaa104
Revises: 253ad71020b3
Create Date: 2025-08-15 11:50:18.443594

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11f05ffaa104'
down_revision: Union[str, Sequence[str], None] = '253ad71020b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('users', 'hashed_password', new_column_name='password')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('users', 'password', new_column_name='hashed_password')
    pass
