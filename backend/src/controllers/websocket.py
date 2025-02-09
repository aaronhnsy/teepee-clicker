import asyncio
import json
from typing import AsyncGenerator

from litestar import websocket
from litestar.handlers import send_websocket_stream

from src.exceptions import UserNotFoundException
from src.models.user import User
from src.types import State, Websocket


__all__ = ["websocket_handler"]


@websocket("/")
async def websocket_handler(socket: Websocket, state: State) -> None:

    try:
        await User.get(state, name=socket.cookies.get("username"))
    except UserNotFoundException:
        await socket.send_json({"error": "user not found"})
        await socket.close()
        return
    await socket.accept()

    async def handle_stream() -> AsyncGenerator[str, None]:
        while True:
            yield json.dumps({
                "pets": await User.get_global_pet_count(state),
            })
            await asyncio.sleep(1)

    async def handle_receive() -> None:
        async for event in socket.iter_json():
            print(f"{socket.client}: {event}")

    async with asyncio.TaskGroup() as task_group:
        task_group.create_task(send_websocket_stream(socket=socket, stream=handle_stream()))
        task_group.create_task(handle_receive())
