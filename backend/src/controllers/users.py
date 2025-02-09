from litestar import Controller, get, post

from src.models import BaseModel, User
from src.types import Request, State


__all__ = ["UserController"]


class CreateUserRequestData(BaseModel):
    username: str
    password: str


class UserController(Controller):
    path = "/users"

    @post(exclude_from_auth=True)
    async def create_user(
        self, state: State,
        data: CreateUserRequestData
    ) -> User:
        return await User.create(
            state,
            username=data.username, password=data.password
        )

    @get(path="/me")
    async def get_user(self, request: Request) -> User:
        return request.user
