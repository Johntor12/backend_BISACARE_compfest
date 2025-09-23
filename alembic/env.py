import asyncio
import os
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

# ----------------------------
# CONFIG LOGGING
# ----------------------------
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ----------------------------
# IMPORT METADATA
# ----------------------------
# Pastikan Base metadata dari project kamu diimport
from infrastructure.db.connection import Base
# import semua model supaya metadata lengkap
from infrastructure.db.models.user_model import UserModel
from infrastructure.db.models.claim_model import ClaimModel
from infrastructure.db.models.testi_model import TestiModel
from infrastructure.db.models.insurance_form_model import InsuranceFormModel
from infrastructure.db.models.slip_model import SlipModel
from infrastructure.db.models.chat_model import ChatMessageModel, ChatSessionModel
from infrastructure.db.models.claim_document_model import ClaimDocumentModel
from infrastructure.db.models.claim_event_model import ClaimEventModel

target_metadata = Base.metadata

# ----------------------------
# DATABASE URL
# ----------------------------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://neondb_owner:npg_Diz4OWJ3VoAk@ep-noisy-sea-adgcl31n.c-2.us-east-1.aws.neon.tech/neondb?ssl=require"
)

# ----------------------------
# OFFLINE MIGRATION (tidak perlu koneksi)
# ----------------------------
def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# ----------------------------
# HELPER SYNC FUNCTION UNTUK ONLINE MIGRATION
# ----------------------------
def run_migrations_sync(connection: Connection):
    """Fungsi sync yang dipanggil di run_sync"""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,  # penting untuk autogenerate enum/column type changes
    )
    with context.begin_transaction():
        context.run_migrations()

# ----------------------------
# ONLINE MIGRATION (async engine)
# ----------------------------
def run_migrations_online():
    """Run migrations using async engine."""
    connectable = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
        echo=True  # bisa diubah False di production
    )

    async def do_run_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(run_migrations_sync)
        await connectable.dispose()

    asyncio.run(do_run_migrations())

# ----------------------------
# MAIN EXECUTION
# ----------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
