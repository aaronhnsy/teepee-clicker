import itsdangerous
from litestar.middleware import AbstractAuthenticationMiddleware, AuthenticationResult, DefineMiddleware
from litestar.status_codes import HTTP_401_UNAUTHORIZED

from src.exceptions import ReasonException
from src.models import User
from src.security import unsign_session_id
from src.types import Connection, State


__all__ = ["AuthenticationMiddleware"]


class _AuthenticationMiddleware(AbstractAuthenticationMiddleware):

    async def authenticate_request(self, connection: Connection) -> AuthenticationResult:
        state: State = connection.app.state  # pyright: ignore[reportAssignmentType]
        # check if the session_id is in the cookies
        session_id = connection.cookies.get("__session_id")
        if session_id is None:
            raise ReasonException(
                HTTP_401_UNAUTHORIZED,
                reason="You must provide a valid '__session_id' cookie to use this endpoint.",
            )
        # check if the session_id is valid
        try:
            data = unsign_session_id(session_id)
            session = await state.database.fetchrow(
                "SELECT * FROM sessions WHERE user_id = $1 AND secret = $2",
                data["user_id"], data["secret"],
            )
            if session is None:
                raise ValueError
        except itsdangerous.SignatureExpired:
            raise ReasonException(
                HTTP_401_UNAUTHORIZED,
                reason="The provided session id has expired.",
            )
        except (itsdangerous.BadSignature, ValueError):
            raise ReasonException(
                HTTP_401_UNAUTHORIZED,
                reason="The provided session id is invalid.",
            )
        # fetch the user from the database and return the result
        user = await User.get(state, data["user_id"])
        return AuthenticationResult(user=user, auth=None)


AuthenticationMiddleware = DefineMiddleware(
    _AuthenticationMiddleware,
    exclude=["schema"]
)
