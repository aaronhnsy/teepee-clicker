from typing import TYPE_CHECKING, TypedDict
import asqlite
from litestar.connection import ASGIConnection
from litestar.datastructures import State as _State

from litestar.handlers import HTTPRouteHandler

if TYPE_CHECKING:
    from src.models.user import User

__all__ = ["Database", "Connection", "State", "SessionData"]

type Database = asqlite.Cursor
type Connection = ASGIConnection[HTTPRouteHandler, User, None, State]


class State(_State):
    database: Database


class SessionData(TypedDict):
    user_id: int
    secret: str
