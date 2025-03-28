from litestar import Litestar

from src.controllers import router
from src.exceptions import exception_handlers
from src.middleware import AuthenticationMiddleware
from src.openapi import openapi_config
from src.snowflakes import SnowflakeGenerator
from src.storage import postgresql_lifespan


__all__ = ["teepee"]


teepee: Litestar = Litestar(
    lifespan=[postgresql_lifespan],
    route_handlers=[router],
    middleware=[AuthenticationMiddleware],
    exception_handlers=exception_handlers,
    openapi_config=openapi_config,
)
teepee.state.snowflake = SnowflakeGenerator(machine_id=0, process_id=0)
