from litestar import Controller, post, get

from src.models import User
from src.models.base import BaseModel
from src.types import State, Request


class CreateUserRequestData(BaseModel):
    name: str


class UserController(Controller):
    path = "/user"

    @get()
    async def get_user_pets(self, request: Request) -> int:
        return request.user.pets

    @post(exclude_from_auth=True)
    async def create_user(self, state: State, data: CreateUserRequestData) -> User:
        return await User.create(state, name=data.name)
