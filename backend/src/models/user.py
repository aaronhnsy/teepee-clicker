from __future__ import annotations

import asyncpg

from src.exceptions import UserNotFoundException
from src.models.base import BaseModel
from src.models.upgrade import UpgradeType, Upgrade
from src.types import State


__all__ = ["User"]


class User(BaseModel):
    name: str
    pets: int

    @classmethod
    async def get(
        cls,
        state: State,
        /, *,
        name: str
    ) -> User:
        data: asyncpg.Record | None = await state.database.fetchrow(
            "SELECT * FROM users WHERE name = $1",
            name
        )
        if data is None:
            raise UserNotFoundException
        return User.model_validate({**data})

    @classmethod
    async def get_top_10_pets(cls, state: State, /) -> dict[str, int]:
        data: list[asyncpg.Record] | None = await state.database.fetch(
            "SELECT name, pets FROM users ORDER BY pets DESC LIMIT 10",
        )

        return {record["name"]: record["pets"] for record in data}

    async def remove_pets(self, state: State, /, *, count: float) -> None:
        await state.database.execute(
            "UPDATE users SET pets = pets - $1 WHERE name = $2",
            count, self.name
        )

    @classmethod
    async def get_global_pet_count(cls, state: State) -> int:
        data: asyncpg.Record | None = await state.database.fetchrow(
            "SELECT SUM(pets) FROM users"
        )
        return data["sum"]

    @classmethod
    async def create(cls, state: State, /, *, name: str) -> User:
        try:
            user_data: asyncpg.Record | None = await state.database.fetchrow(
                "INSERT INTO users (name, pets) VALUES ($1, $2) RETURNING *", name, 0
            )
        except asyncpg.UniqueViolationError:
            raise UserNotFoundException

        user: User = cls.model_validate({**user_data})

        for x in UpgradeType:
            await state.database.execute(
                "INSERT INTO upgrades (type, owner, count) VALUES ($1, $2, $3)", x, user.name, 0
            )

        return user

    async def update_pets(self, state: State, /, *, count: float) -> None:
        await state.database.execute(
            "UPDATE users SET pets = $1 WHERE name = $2",
            count, self.name
        )

    async def set_upgrades(self, state: State, /, *, upgrades: list[Upgrade]) -> None:
        for upgrade in upgrades:
            await state.database.execute(
                "UPDATE upgrades SET count = $1 WHERE owner = $2 AND type = $3",
                upgrade.count, self.name, upgrade.type
            )
