from litestar.middleware import AbstractAuthenticationMiddleware, AuthenticationResult, DefineMiddleware

from src.exceptions import InvalidUserSecretException
from src.models.upgrade import Upgrade
from src.types.types import Connection, State

__all__ = ["AuthMiddleware"]


class _AuthMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(self, connection: Connection) -> AuthenticationResult:
        state: State = connection.app.state  # pyright: ignore[reportAssignmentType]
        username: str | None = connection.cookies.get("username")
        if username is None:
            raise InvalidUserSecretException
        user: tuple[str, int, list[Upgrade]] = state.database.execute(
            "SELECT * FROM users WHERE username = ?", [username]
        ).fetchone()
        return AuthenticationResult(user=user, auth=None)


AuthMiddleware = DefineMiddleware(_AuthMiddleware)
