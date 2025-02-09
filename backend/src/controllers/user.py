from litestar import Controller

from src.models.base import BaseModel


class CreateUserRequestData(BaseModel):
    name: str


class UserController(Controller):
    path = "/user"

    # @get()
    # async def get_user(self, request: Request) -> User:
    #     return request.user
    #
    # @post(exclude_from_auth=True)
    # async def creater_user(self, state: State, data: CreateUserRequestData) -> User:
    #     return await User.create(state, name=data.name)
