import sqlite3
from typing import Any

import asqlite
from .types import State

__all__ = ["query_fetchone", "query_fetchall"]


async def query_fetchone(state: State, /, *, query: str, params: tuple[Any, ...] | None = None) -> sqlite3.Row:
    cursor: asqlite.Cursor
    if params is None:
        cursor = await state.database.execute(query)
    else:
        cursor = await state.database.execute(query, params)
    row: sqlite3.Row = await cursor.fetchone()
    return row


async def query_fetchall(state: State, /, *, query: str, params: tuple[Any, ...] | None = None) -> list[sqlite3.Row]:
    cursor: asqlite.Cursor
    if params is None:
        cursor = await state.database.execute(query)
    else:
        cursor = await state.database.execute(query, params)
    rows: list[sqlite3.Row] = await cursor.fetchall()
    return rows


def dict_factory(cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict[Any, Any]:
    d: dict[Any, Any] = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
