"""renaming hashed_password to password v1

Revision ID: 4b5f65a803bc
Revises: 458ada41951f
Create Date: 2025-08-15 11:46:59.752659

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b5f65a803bc'
down_revision: Union[str, Sequence[str], None] = '458ada41951f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
