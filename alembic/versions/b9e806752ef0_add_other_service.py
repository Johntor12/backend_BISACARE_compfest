"""add other service

Revision ID: b9e806752ef0
Revises: 7dbe5ff4f970
Create Date: 2025-08-18 11:35:31.018060

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9e806752ef0'
down_revision: Union[str, Sequence[str], None] = '7dbe5ff4f970'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


insurance_type_enum = sa.Enum(
    "rawat_jalan", 
    "rawat_inap", 
    "igd", 
    "lainnya",
    name="insurance_type_enum"
)

def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint("chat_messages_session_id_fkey", "chat_messages", type_="foreignkey")

    op.drop_index(op.f('ix_chat_sessions_user_id'), table_name='chat_sessions')
    op.drop_table('chat_sessions')
    op.drop_index(op.f('ix_chat_messages_session_id'), table_name='chat_messages')
    op.drop_table('chat_messages')
    op.drop_index(op.f('ix_claim_documents_id'), table_name='claim_documents')
    op.drop_table('claim_documents')
    op.drop_index(op.f('ix_claim_events_id'), table_name='claim_events')
    op.drop_table('claim_events')


    # Create Table
    op.create_table(
        "insurance_forms",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("patient_name", sa.String(100), nullable=False),
        sa.Column("insurance_type", insurance_type_enum, nullable=False),
        sa.Column("other_service", sa.String(100), nullable=True),  # opsional
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())
    )

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("insurance_forms")
    pass
