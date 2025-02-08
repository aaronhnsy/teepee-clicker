from typing import TYPE_CHECKING
import asqlite
from litestar.connection import ASGIConnection
from litestar.datastructures import State as _State
from litestar import WebSocket as _WebSocket
from litestar import Request as _Request

from litestar.handlers import HTTPRouteHandler

if TYPE_CHECKING:
    from src.models.user import User

__all__ = ["Database", "Connection", "State", "Request", "WebSocket"]

type Database = asqlite.Cursor
type Connection = ASGIConnection[HTTPRouteHandler, User, None, State]
type Request = _Request[User, None, State]
type WebSocket = _WebSocket[User, None, State]


class State(_State):
    database: Database
