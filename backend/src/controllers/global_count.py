from litestar import Controller, get

from src.models.user import User
from src.types import State


class GlobalPetCounter(Controller):
    path = "/pets"

    @get()
    async def get_global_pets(self, state: State) -> int:
        return await User.get_total_pets(state)
