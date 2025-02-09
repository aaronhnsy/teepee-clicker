from litestar import Controller, post

from src.models import BaseModel, Session
from src.types import State


__all__ = ["SessionsController"]


class CreateSessionRequestData(BaseModel):
    username: str
    password: str
    description: str


class SessionsController(Controller):
    path = "/sessions"

    @post(exclude_from_auth=True)
    async def create_session(
        self, state: State,
        data: CreateSessionRequestData
    ) -> str:
        return await Session.create(
            state,
            username=data.username, password=data.password,
            description=data.description,
        )
