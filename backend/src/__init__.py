from litestar import Litestar

from src.controllers import router
from src.middleware import AuthenticationMiddleware
from src.openapi import openapi_config
from src.storage import postgresql_lifespan


__all__ = ["teepee_clicker"]


teepee_clicker: Litestar = Litestar(
    lifespan=[postgresql_lifespan],
    route_handlers=[router],
    middleware=[AuthenticationMiddleware],
    openapi_config=openapi_config,
)
