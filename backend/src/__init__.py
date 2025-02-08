from litestar.channels import ChannelsPlugin
from src.controllers import router
from litestar import Litestar
from litestar.channels.backends.memory import MemoryChannelsBackend

from src.middleware import AuthMiddleware
from src.storage import sqlite_lifespan

__all__ = ["teepee_clicker"]

teepee_clicker: Litestar = Litestar(
    lifespan=[sqlite_lifespan],
    route_handlers=[router],
    middleware=[AuthMiddleware],
    plugins=[ChannelsPlugin(channels=["chat"], backend=MemoryChannelsBackend(history=10))],
)
