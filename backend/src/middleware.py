import sqlite3
from litestar.middleware import AbstractAuthenticationMiddleware, AuthenticationResult, DefineMiddleware
from pydantic import ValidationError

from src.exceptions import UserNotFoundException
from src.models.user import User
from src.types import Connection, State
from src.util import query_fetchone

__all__ = ["AuthMiddleware"]


class _AuthMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(self, connection: Connection) -> AuthenticationResult:
        state: State = connection.app.state  # pyright: ignore[reportAssignmentType]
        username: str | None = connection.cookies.get("username")
        if username is None:
            raise UserNotFoundException
        possible_user: sqlite3.Row = await query_fetchone(
            state, query="SELECT * FROM users WHERE name = ?", params=(username,)
        )
        user: User
        try:
            user = User.model_validate(possible_user)
        except ValidationError:
            raise UserNotFoundException

        return AuthenticationResult(user=user, auth=None)


AuthMiddleware = DefineMiddleware(_AuthMiddleware, exclude="/ws")
