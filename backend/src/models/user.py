from __future__ import annotations

import asyncpg
import pydantic
from litestar.status_codes import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from src.exceptions import ReasonException
from src.models.base import BaseModel
from src.models.upgrade import Upgrade, UpgradeType
from src.security import hash_password
from src.types import State


__all__ = ["User"]


class User(BaseModel):
    id: int
    name: str
    pets: int

    @pydantic.field_serializer(*["id", "pets"], check_fields=False, when_used="json-unless-none")
    def serialize_ints(self, value: int, /) -> str:
        return str(value)

    # methods

    @classmethod
    async def create(
        cls, state: State, /,
        *, username: str, password: str
    ) -> User:
        try:
            data: asyncpg.Record | None = await state.database.fetchrow(
                "INSERT INTO users (id, name, password) VALUES ($1, $2, $3) RETURNING *",
                state.snowflake.generate(), username, hash_password(password)
            )
        except asyncpg.UniqueViolationError:
            raise ReasonException(
                HTTP_409_CONFLICT,
                reason="A user with the specified username already exists.",
            )
        user = User.model_validate({**data})
        await state.database.executemany(
            "INSERT INTO upgrades (user_id, upgrade_type) VALUES ($1, $2)",
            [(user.id, upgrade_type) for upgrade_type in UpgradeType]
        )
        return user

    @classmethod
    async def get(cls, state: State, _id: int, /) -> User:
        data = await state.database.fetchrow(
            "SELECT id, name, pets FROM users WHERE id = $1",
            _id,
        )
        if data is None:
            raise ReasonException(
                HTTP_404_NOT_FOUND,
                reason="A user with the specified id does not exist.",
            )
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
