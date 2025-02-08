from litestar.status_codes import HTTP_401_UNAUTHORIZED, HTTP_418_IM_A_TEAPOT


__all__ = ["ReasonException", "InvalidUserSecretException", "ApplyUpgradeException"]


class ReasonException(Exception):
    def __init__(self, status_code: int, /, *, reason: str) -> None:
        super().__init__(reason)
        self.status_code: int = status_code
        self.reason: str = reason


InvalidUserSecretException = ReasonException(HTTP_401_UNAUTHORIZED, reason="Invalid or missing user secret!")
ApplyUpgradeException = ReasonException(HTTP_418_IM_A_TEAPOT, reason="Unable to apply upgrade idk")
