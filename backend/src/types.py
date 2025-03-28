from typing import TYPE_CHECKING, TypedDict

import asyncpg
from litestar import Request as _Request
from litestar import WebSocket as _Websocket
from litestar.connection import ASGIConnection
from litestar.datastructures import State as _State
from litestar.handlers.http_handlers import HTTPRouteHandler

from src.snowflakes import SnowflakeGenerator


if TYPE_CHECKING:
    from src.models import User


__all__ = [
    "Database",
    "Connection",
    "Request",
    "Websocket",
    "State",
    "SessionData",
]


type Database = asyncpg.Pool[asyncpg.Record]
type Connection = ASGIConnection[HTTPRouteHandler, User, None, State]
type Request = _Request[User, None, State]
type Websocket = _Websocket[User, None, State]


class State(_State):
    database: Database
    snowflake: SnowflakeGenerator


class SessionData(TypedDict):
    user_id: int
    secret: str
