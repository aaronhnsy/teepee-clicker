import asyncio
import json
from typing import AsyncGenerator

from litestar import websocket
from litestar.handlers import send_websocket_stream
from pydantic import ValidationError

from src.models import Upgrade
from src.models.user import User
from src.types import State, Websocket


__all__ = ["websocket_handler"]


@websocket("/")
async def websocket_handler(socket: Websocket, state: State) -> None:

    async def handle_stream() -> AsyncGenerator[str, None]:
        while True:
            total_pets: int = await User.get_global_pet_count(state)
            top_ten_petters: dict[str, int] = await User.get_top_10_pets(state)
            other_pets: int = total_pets - sum(top_ten_petters.values())
            yield json.dumps({
                "total_pets": str(total_pets),
                "top_ten_petters": str(top_ten_petters),
                "other_pets": str(other_pets)
            })
            await asyncio.sleep(1)

    async def handle_receive() -> None:
        async for event in socket.iter_json():
            if "pets" in event.keys():
                await websocket.user.update_pets(state, count=event.get("pets"))
            if "upgrades" in event.keys():
                try:
                    user_upgrades: list[Upgrade] = [Upgrade.model_validate({**upgrade}) for upgrade in event["upgrades"]]
                except ValidationError:
                    await socket.send_json({"error": "invalid upgrade"})
                    return
                await websocket.user.set_upgrades(state, upgrades=user_upgrades)
            print(f"{socket.client}: {event}")
        await asyncio.sleep(5)

    async with asyncio.TaskGroup() as task_group:
        task_group.create_task(send_websocket_stream(socket=socket, stream=handle_stream()))
        task_group.create_task(handle_receive())
