import pydantic


__all__ = ["BaseModel"]


class BaseModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True, strict=True)
