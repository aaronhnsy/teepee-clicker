from litestar import Router

from .global_count import GlobalPetCounter
from .user import UserController
from .websocket import websocket_handler


__all__ = ["router"]


api_router = Router(
    path="/api",
    route_handlers=[GlobalPetCounter, UserController]
)
websocket_router = Router(
    path="/websocket",
    route_handlers=[websocket_handler]
)
router = Router(
    path="/",
    route_handlers=[api_router, websocket_router]
)
