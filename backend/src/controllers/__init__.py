from litestar import Router

from src.controllers.user import UserController

from .global_count import GlobalPetCounter


__all__ = ["router"]

router = Router(path="/api/", route_handlers=[GlobalPetCounter, UserController])
