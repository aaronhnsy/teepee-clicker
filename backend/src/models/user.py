from __future__ import annotations

import sqlite3


from src.exceptions import ApplyUpgradeException
from src.models.base import BaseModel
from src.models.upgrade import Upgrade
from src.types import State
from src.util import query_fetchall, query_fetchone

__all__ = ["User"]


class User(BaseModel):
    name: str
    pet_count: int
    current_multiplier: float

    async def get_upgrades(self, state: State, /) -> list[Upgrade]:
        data: list[sqlite3.Row] = await query_fetchall(
            state,
            query="SELECT upgrades.* FROM upgrades INNER JOIN user_upgrades uu on upgrades.name = uu.upgrade WHERE uu.name = ?",
            params=[self.name],
        )
        return [Upgrade.model_validate({**upgrade}) for upgrade in data]

    async def apply_upgrade(self, state: State, /, *, upgrade: Upgrade) -> User:
        new_multiplier: float = self.current_multiplier * upgrade.multiplier

        try:
            await state.database.execute(
                "UPDATE users SET current_multiplier = ? WHERE name = ?", [new_multiplier, self.name]
            )
        except sqlite3.IntegrityError:
            raise ApplyUpgradeException

        self.current_multiplier = new_multiplier
        return self

    @classmethod
    async def get_total_pets(cls, state: State, /) -> int:
        data: sqlite3.Row = await query_fetchone(state, query="SELECT (SELECT SUM(pet_count)) AS pet_count FROM users")
        return data["pet_count"]
