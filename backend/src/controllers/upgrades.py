from litestar import Controller, get, post

from src.models import BaseModel, Upgrade, UpgradeType
from src.types import Request, State


class PurchaseUpgradeRequest(BaseModel):
    type: UpgradeType


class UpgradeController(Controller):
    path = "/upgrade"

    @get()
    async def get_all_upgrades(self, state: State, request: Request) -> list[Upgrade]:
        return await Upgrade.get_all(state, owner=request.user)

    @post()
    async def purchase_upgrade(self, state: State, request: Request, data: PurchaseUpgradeRequest) -> None:
        upgrade: Upgrade = await Upgrade.get(state, type=data.type, owner=request.user)
        await upgrade.purchase(state, owner=request.user)
