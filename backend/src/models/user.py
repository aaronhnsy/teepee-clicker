from __future__ import annotations

import sqlite3

from src.exceptions import NotEnoughPetsException, UserAlreadyExistsError, UserNotFoundException
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
            query="""
            SELECT upgrades.* FROM upgrades
            INNER JOIN user_upgrades uu on upgrades.name = uu.upgrade
            WHERE uu.name = ?"
            """,
            params=(self.name,),
        )
        return [Upgrade.model_validate({**upgrade}) for upgrade in data]

    async def purchase_upgrade(self, state: State, /, *, upgrade: Upgrade) -> User:
        if self.pet_count >= upgrade.cost:
            self.pet_count = self.pet_count - upgrade.cost
        else:
            raise NotEnoughPetsException
        new_multiplier: float = self.current_multiplier * upgrade.multiplier

        await state.database.execute(
            "UPDATE users SET current_multiplier = ? WHERE name = ?", [new_multiplier, self.name]
        )

        self.current_multiplier = new_multiplier
        return self

    @classmethod
    async def get_total_pets(cls, state: State, /) -> int:
        data: sqlite3.Row = await query_fetchone(state, query="SELECT (SELECT SUM(pet_count)) AS pet_count FROM users")
        return data["pet_count"]

    @classmethod
    async def get(cls, state: State, /, *, name: str) -> User:
        data: sqlite3.Row = await query_fetchone(state, query="SELECT * FROM users WHERE name = ?", params=(name,))

        if data["name"] is None:
            raise UserNotFoundException

        return User.model_validate(data)

    @classmethod
    async def get_all(cls, state: State, /) -> list[User]:
        data: list[sqlite3.Row] = await query_fetchall(state, query="SELECT * FROM users")
        return [User.model_validate({**user}) for user in data]

    @classmethod
    async def create(cls, state: State, /, *, name: str) -> User:
        data: sqlite3.Row
        try:
            data: sqlite3.Row = await query_fetchone(
                state, query="INSERT INTO users VALUES (?, ?, ?) RETURNING *", params=(name, 0, 1.0)
            )
        except sqlite3.IntegrityError:
            raise UserAlreadyExistsError
        return User.model_validate(data)
