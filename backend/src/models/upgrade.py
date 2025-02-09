from __future__ import annotations

import enum
from typing import Annotated, TYPE_CHECKING

import asyncpg
import pydantic
from litestar.status_codes import HTTP_400_BAD_REQUEST

from src.exceptions import ReasonException
from src.models.base import BaseModel
from src.types import State


if TYPE_CHECKING:
    from src.models import User


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

    @pydantic.computed_field()
    def name(self) -> str:
        return self.type.name.lower().replace("_", " ")

    @pydantic.computed_field()
    def name(self) -> str:
        return self.type.name.lower().replace("_", " ")



    @classmethod
    async def get_all(cls, state: State, /, *, owner: User) -> int:
        data: list[asyncpg.Record] = await state.database.fetch(
            "SELECT COUNT(*) as count FROM upgrades WHERE owner = $1",
            owner.name
        )
        return data

    @classmethod
    async def purchase(cls, state: State, /, *, type: UpgradeType, owner: User) -> None:
        count = await state.database.fetchrow(
            "SELECT COUNT(*) as count FROM upgrades WHERE owner = $1",
            owner.name
        )
        cost = UPGRADE_COSTS[type] * (UPGRADE_COST_MULTIPLIERS[type] * count["count"])
        if owner.pets < cost:
            raise ReasonException(
                HTTP_400_BAD_REQUEST,
                reason="You do not have enough pets to purchase this upgrade.",
            )
        await state.database.execute(
            "INSERT INTO upgrades (type, owner) VALUES ($1, $2)",
            type, owner,
        )
        await owner.remove_pets(state, count=cost)
