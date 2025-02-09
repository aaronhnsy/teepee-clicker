from litestar import Router

from .sessions import SessionsController
from .upgrades import UpgradeController
from .users import UserController
from .websocket import websocket_handler


__all__ = ["router"]


api_router = Router(
    path="/api",
    route_handlers=[UserController, SessionsController, UpgradeController]
)
websocket_router = Router(
    path="/websocket",
    route_handlers=[websocket_handler]
)
router = Router(
    path="/",
    route_handlers=[api_router, websocket_router]
)
