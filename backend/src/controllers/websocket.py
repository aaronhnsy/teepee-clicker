from litestar import websocket_listener
from src.types import WebSocket, State
from src.models.user import User


async def is_valid_user(name: str, state: State, socket: WebSocket) -> None:
    users: list[User] = await User.get_all(state)
    print(users)
    for n in users:
        if n.name == name:
            await socket.accept(headers={"Cookie": name})
        else:
            await socket.close()


@websocket_listener("/ws/upgrade", connection_accept_handler=is_valid_user)
async def handler(data: str) -> str:
    return data
