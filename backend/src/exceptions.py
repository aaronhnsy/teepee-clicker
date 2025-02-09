import http
import traceback
from collections.abc import Callable
from typing import Any

import pydantic
from litestar import MediaType, Response
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from src.types import Request


__all__ = [
    "ReasonException",
    "NotFoundException",
    "Error",
    "exception_handlers",
]

type _ExceptionHandlerResponse = Response[dict[str, Any]]
type _ExceptionHandler[T: Exception] = Callable[[Request, T], _ExceptionHandlerResponse]
type _ExceptionHandlerMapping = dict[
    type[ReasonException | HTTPException | Exception],
    _ExceptionHandler[ReasonException] | _ExceptionHandler[HTTPException] | _ExceptionHandler[Exception],
]


class ReasonException(Exception):

    def __init__(self, status_code: int, /, *, reason: str) -> None:
        super().__init__(reason)
        self.status_code: int = status_code
        self.reason: str = reason


NotFoundException = ReasonException(
    HTTP_404_NOT_FOUND,
    reason="Something related to your request could not be found.",
)


def fmt_status_code(status_code: int) -> str:
    return f"{status_code} ({http.HTTPStatus(status_code).name})"


class Error(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True, strict=True)
    status_code: int
    status_name: str
    reason: str | None


def handle_custom_exception(request: Request, exception: ReasonException) -> _ExceptionHandlerResponse:
    return Response(
        media_type=MediaType.JSON,
        status_code=exception.status_code,
        content=Error(
            status_code=exception.status_code,
            status_name=fmt_status_code(exception.status_code),
            reason=exception.reason,
        ).model_dump(),
    )


def handle_http_exception(request: Request, exception: HTTPException) -> _ExceptionHandlerResponse:
    return Response(
        media_type=MediaType.JSON,
        status_code=exception.status_code,
        content=Error(
            status_code=exception.status_code,
            status_name=fmt_status_code(exception.status_code),
            reason=None,
        ).model_dump(),
    )


def handle_other_exception(request: Request, exception: Exception) -> _ExceptionHandlerResponse:
    status_code = HTTP_500_INTERNAL_SERVER_ERROR
    tb = traceback.format_exception(exception)
    print("".join(tb))
    return Response(
        media_type=MediaType.JSON,
        status_code=status_code,
        content=Error(
            status_code=status_code,
            status_name=fmt_status_code(status_code),
            reason=tb[-1],
        ).model_dump(),
    )


exception_handlers: _ExceptionHandlerMapping = {
    ReasonException: handle_custom_exception,
    HTTPException:   handle_http_exception,
    Exception:       handle_other_exception,
}
