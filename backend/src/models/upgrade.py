from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Annotated

import asyncpg
import pydantic
from litestar.status_codes import HTTP_400_BAD_REQUEST

from src.exceptions import ReasonException
from src.models.base import BaseModel
from src.types import State


if TYPE_CHECKING:
    from src.models import User

__all__ = [
    "UpgradeType",
    "UPGRADE_COSTS",
    "UPGRADE_COST_MULTIPLIERS",
    "Upgrade",
]

class UpgradeType(enum.IntEnum):
    AUTO_PETTER = enum.auto()
    TIPI = enum.auto()
    SLEEPY = enum.auto()
    OPPS = enum.auto()
    HUNGER = enum.auto()
    SCREAM = enum.auto()
    BNUUY = enum.auto()
    STRETCHIES = enum.auto()
    MLEM = enum.auto()


UPGRADE_COSTS: dict[UpgradeType, int] = {
    UpgradeType.AUTO_PETTER: 10,
    UpgradeType.TIPI:        20,
    UpgradeType.SLEEPY:      30,
    UpgradeType.OPPS:        40,
    UpgradeType.HUNGER:      50,
    UpgradeType.SCREAM:      60,
    UpgradeType.BNUUY:       70,
    UpgradeType.STRETCHIES:  80,
    UpgradeType.MLEM:        90,
}
UPGRADE_COST_MULTIPLIERS: dict[UpgradeType, float] = {
    UpgradeType.AUTO_PETTER: 1.5,
    UpgradeType.TIPI:        2.0,
    UpgradeType.SLEEPY:      2.5,
    UpgradeType.OPPS:        3.0,
    UpgradeType.HUNGER:      3.5,
    UpgradeType.SCREAM:      4.0,
    UpgradeType.BNUUY:       4.5,
    UpgradeType.STRETCHIES:  5.0,
    UpgradeType.MLEM:        5.5,
}


class Upgrade(BaseModel):
    type: Annotated[
        UpgradeType,
        pydantic.Field(strict=False),
    ]
    owner: str
    count: int

    @pydantic.computed_field()
    def upgrade_name(self) -> str:
        return self.type.name.lower().replace("_", " ")

    @classmethod
    async def get(cls, state: State, /, *, type: UpgradeType, owner: User) -> Upgrade:
        data: asyncpg.Record = await state.database.fetchrow(
            "SELECT * FROM upgrades WHERE owner = $1 AND type = $2",
            owner.name, type
        )
        return Upgrade.model_validate({**data})


    @classmethod
    async def get_all(cls, state: State, /, *, owner: User) -> list[Upgrade]:
        data: list[asyncpg.Record] = await state.database.fetch(
            "SELECT * FROM upgrades WHERE owner = $1",
            owner.name
        )
        return [Upgrade.model_validate({**upgrade}) for upgrade in data]

    async def purchase(self, state: State, /, *, owner: User) -> None:
        cost = UPGRADE_COSTS[self.type] * (UPGRADE_COST_MULTIPLIERS[self.type] * self.count + 1)
        if owner.pets < cost:
            raise ReasonException(
                HTTP_400_BAD_REQUEST,
                reason="You do not have enough pets to purchase this upgrade.",
            )
        await state.database.execute(
            "UPDATE upgrades SET count = $1 WHERE owner = $2 AND type = $3",
            self.count + 1, owner.name, self.type
        )
        await owner.remove_pets(state, count=cost)
