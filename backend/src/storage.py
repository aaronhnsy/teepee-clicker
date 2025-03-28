import contextlib
from collections.abc import AsyncGenerator

import asyncpg
from litestar import Litestar

from src.config import CONFIG
from src.types import Database


__all__ = ["postgresql_lifespan"]


@contextlib.asynccontextmanager
async def postgresql_lifespan(app: Litestar) -> AsyncGenerator[None]:
    # runs when the app starts
    database: Database = await asyncpg.create_pool(  # pyright: ignore[reportAssignmentType]
        CONFIG.storage.postgres_dsn,
        command_timeout=300,
        min_size=0, max_size=20,
    )
    app.state.database = database
    # runs when the app stops
    try:
        yield
    finally:
        await app.state.database.close()
