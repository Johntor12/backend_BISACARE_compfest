"""change str input_type to literal

Revision ID: 7dbe5ff4f970
Revises: 9caf7c9b0ad8
Create Date: 2025-08-18 11:30:15.534615

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7dbe5ff4f970'
down_revision: Union[str, Sequence[str], None] = '9caf7c9b0ad8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
