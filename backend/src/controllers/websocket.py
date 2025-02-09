import asyncio
import json
from typing import AsyncGenerator

import asyncpg
from litestar import websocket
from litestar.handlers import send_websocket_stream
from pydantic import ValidationError

from src.exceptions import UserNotFoundException
from src.models import Upgrade
from src.models.user import User
from src.types import State, Websocket


__all__ = ["websocket_handler"]


@websocket("/")
async def websocket_handler(socket: Websocket, state: State) -> None:
    # Maybe catch RuntimeError here since that gets thrown when socket.close is called
    data: asyncpg.Record | None = await state.database.fetchrow(
        "SELECT * FROM users WHERE name = $1",
        socket.cookies.get("username")
    )

    if data is None:
        await socket.send_json({"error": "User not found"})
        await socket.close()
        return
    await socket.accept()

    async def handle_stream() -> AsyncGenerator[str, None]:
        while True:
            total_pets: int = await User.get_global_pet_count(state)
            top_10_pets: dict[str, int] = await User.get_top_10_pets(state)
            other_pets: int = total_pets - sum(top_10_pets.values())
            yield json.dumps({
                "pets": await User.get_global_pet_count(state),
                "top_10_pets": await User.get_top_10_pets(state),
                "other_pets": other_pets
            })
            await asyncio.sleep(1)

    async def handle_receive() -> None:
        async for event in socket.iter_json():
            if "pet_count" not in event.keys():
                await socket.send_json({"error": "new count is not provided"})
                return
            elif "upgrades" not in event.keys():
                await socket.send_json({"error": "upgrade list is not provided"})
                return
            elif "name" not in event.keys():
                await socket.send_json({"error": "name is not provided"})
                return
            try:
                user_upgrades: list[Upgrade] = [Upgrade.model_validate({**upgrade}) for upgrade in event["upgrades"]]
            except ValidationError:
                await socket.send_json({"error": "invalid upgrade"})
                return

            user: User = await User.get(state, name=event.get("name"))
            await user.update_pets(state, count=event.get("pet_count"))
            await user.set_upgrades(state, upgrades=user_upgrades)
            print(f"{socket.client}: {event}")
        await asyncio.sleep(5)
    async with asyncio.TaskGroup() as task_group:
        task_group.create_task(send_websocket_stream(socket=socket, stream=handle_stream()))
        task_group.create_task(handle_receive())
