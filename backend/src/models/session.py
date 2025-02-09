import secrets

from litestar.status_codes import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from src.exceptions import ReasonException
from src.models import BaseModel
from src.security import sign_session_id, verify_password
from src.types import State


__all__ = ["Session"]


class Session(BaseModel):

    @classmethod
    async def create(
        cls, state: State,
        username: str,
        password: str,
        description: str,
    ) -> str:
        data = await state.database.fetchrow(
            "SELECT id, password FROM users WHERE name = $1",
            username,
        )
        if data is None:
            raise ReasonException(
                HTTP_404_NOT_FOUND,
                reason="A user with the specified username does not exist.",
            )
        if verify_password(password, data["password"]) is False:
            raise ReasonException(
                HTTP_401_UNAUTHORIZED,
                reason="The specified username and password do not match.",
            )
        secret = secrets.token_hex(32)
        session_id = sign_session_id({"user_id": data["id"], "secret": secret})
        await state.database.execute(
            "INSERT INTO sessions (user_id, secret, description) VALUES ($1, $2, $3)",
            data["id"],
            secret,
            description,
        )
        return session_id
