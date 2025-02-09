import contextlib
from collections.abc import AsyncGenerator

import asyncpg
from litestar import Litestar

from src.types import Database


__all__ = ["postgresql_lifespan"]


@contextlib.asynccontextmanager
async def postgresql_lifespan(app: Litestar) -> AsyncGenerator[None]:
    # runs when the app is started
    database: Database = await asyncpg.create_pool(  # pyright: ignore[reportAssignmentType]
        "postgres://aaronhnsy:cc7acf8e7a1355b1eb7a00908c24ebcf283c6a33505d4685ba2a2700a0565733@aarons-server:5432/teepee",
        command_timeout=300,
        min_size=0, max_size=20,
    )
    app.state.database = database
    # runs when the app is stopped
    try:
        yield
    finally:
        await app.state.database.close()
