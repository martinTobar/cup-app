from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
import os
from dotenv import load_dotenv
from sqlmodel import SQLModel

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# This sets up logging configurations if necessary
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for Alembic migrations
target_metadata = SQLModel.metadata
print(target_metadata)


def run_migrations_offline():
    context.configure(
        url=DATABASE_URL, target_metadata=target_metadata, literal_binds=True
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    print("offline mode")
    run_migrations_offline()
else:
    print("online mode")
    run_migrations_online()
