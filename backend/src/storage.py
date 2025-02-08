from collections.abc import AsyncGenerator
import contextlib
from litestar import Litestar

import asqlite

__all__ = ["sqlite_lifespan"]


@contextlib.asynccontextmanager
async def sqlite_lifespan(app: Litestar) -> AsyncGenerator[None]:
    database_pool: asqlite.Pool = await asqlite.create_pool("lole")
    stuff = await database_pool.acquire()
    app.state.database = await stuff.cursor()
    try:
        yield
    finally:
        await app.state.database.close()
