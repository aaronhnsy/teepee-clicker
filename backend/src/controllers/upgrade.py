from litestar import Controller, get
from src.types import State
from src.models import Upgrade


class UpgradeController(Controller):
    path = "/upgrade"

    # @get()
    # async def get_all_upgrades(self, state: State) -> list[Upgrade]:
    #     return await Upgrade.get(state)
