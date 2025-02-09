from litestar.middleware import AbstractAuthenticationMiddleware, AuthenticationResult, DefineMiddleware

from src.exceptions import UserNotFoundException
from src.models.user import User
from src.types import Connection, State


__all__ = ["AuthenticationMiddleware"]


class _AuthenticationMiddleware(AbstractAuthenticationMiddleware):

    async def authenticate_request(self, connection: Connection) -> AuthenticationResult:
        state: State = connection.app.state  # pyright: ignore[reportAssignmentType]
        username: str | None = connection.cookies.get("username")
        try:
            user = await User.get(state, name=username)
        except UserNotFoundException:
            raise UserNotFoundException()
        return AuthenticationResult(user=user, auth=None)


AuthenticationMiddleware = DefineMiddleware(
    _AuthenticationMiddleware,
    exclude=["schema", "websocket"]
)
