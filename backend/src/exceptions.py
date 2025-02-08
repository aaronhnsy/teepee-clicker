from litestar.status_codes import (
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_409_CONFLICT,
)


__all__ = [
    "ReasonException",
    "InvalidUserSecretException",
    "NotEnoughPetsException",
    "UserNotFoundException",
    "UserAlreadyExistsError",
]


class ReasonException(Exception):
    def __init__(self, status_code: int, /, *, reason: str) -> None:
        super().__init__(reason)
        self.status_code: int = status_code
        self.reason: str = reason


InvalidUserSecretException = ReasonException(HTTP_401_UNAUTHORIZED, reason="Invalid or missing user secret!")
NotEnoughPetsException = ReasonException(
    HTTP_406_NOT_ACCEPTABLE, reason="You don't have enough pets to purchase this upgrade!"
)
UserNotFoundException = ReasonException(HTTP_404_NOT_FOUND, reason="User could not be found!")
UserAlreadyExistsError = ReasonException(HTTP_409_CONFLICT, reason="User with that name already exists!")
