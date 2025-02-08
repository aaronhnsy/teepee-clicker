from __future__ import annotations

__all__ = ["Upgrade"]


import sqlite3
from pydantic import BaseModel


from src.types import State
from src.util import query_fetchone, query_fetchall


class Upgrade(BaseModel):
    name: int
    cost: int
    multiplier: float

    @classmethod
    async def get_upgrade(cls, state: State, /, *, name: str) -> Upgrade:
        data: sqlite3.Row = await query_fetchone(state, query="SELECT * FROM upgrades WHERE name = ?", params=[name])
        return Upgrade.model_validate(data)

    @classmethod
    async def get_all_upgrades(cls, state: State, /) -> list[Upgrade]:
        data: list[sqlite3.Row] = await query_fetchall(state, query="SELECT * FROM upgrades")
        return [Upgrade.model_validate({**upgrade}) for upgrade in data]
