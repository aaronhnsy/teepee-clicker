from collections.abc import AsyncGenerator
import contextlib
from litestar import Litestar
from litestar.channels import ChannelsPlugin
import asqlite
from litestar.exceptions import WebSocketDisconnect
from src.types import WebSocket

from src.util import dict_factory

__all__ = ["sqlite_lifespan"]


@contextlib.asynccontextmanager
async def sqlite_lifespan(app: Litestar) -> AsyncGenerator[None]:
    database_pool: asqlite.Pool = await asqlite.create_pool("lole")
    conn: asqlite.ProxiedConnection = await database_pool.acquire()
    # because why the fuck does sqlite return stuff as tuples
    conn._conn.row_factory = dict_factory  # pyright: ignore[reportPrivateUsage]
    app.state.database = await conn.cursor()
    try:
        yield
    finally:
        await app.state.database.close()


@contextlib.asynccontextmanager
async def chat_room_lifespan(socket: WebSocket, channels: ChannelsPlugin) -> AsyncGenerator[None]:
    async with channels.start_subscription("chat", history=10) as subscriber:
        try:
            async with subscriber.run_in_background(socket.send_data):
                yield
        except WebSocketDisconnect:
            return
