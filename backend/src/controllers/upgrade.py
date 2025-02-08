from litestar import Controller, get

from src.models.upgrade import Upgrade
from src.types import State


class UpgradeController(Controller):
    path = "/upgrade"

    @get()
    async def get_all_upgrades(self, state: State) -> list[Upgrade]:
        return await Upgrade.get_all_upgrades(state)
