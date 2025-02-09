from __future__ import annotations

import asyncpg

from src.exceptions import UserNotFoundException
from src.models.base import BaseModel
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

    async def remove_pets(self, state: State, /, *, count: int) -> None:
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
