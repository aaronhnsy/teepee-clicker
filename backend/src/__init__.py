from src.controllers import router
from litestar import Litestar

from src.storage import sqlite_lifespan

__all__ = ["teepee_clicker"]

teepee_clicker: Litestar = Litestar(lifespan=[sqlite_lifespan], route_handlers=[router])
