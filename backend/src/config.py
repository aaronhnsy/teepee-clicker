import pathlib
import sys
import tomllib
from typing import Annotated

import pydantic


__all__ = ["CONFIG"]


class Storage(pydantic.BaseModel):
    postgres_dsn: Annotated[str, pydantic.PostgresDsn]


class Security(pydantic.BaseModel):
    itsdangerous_secret: str


class Config(pydantic.BaseModel):
    storage: Storage
    security: Security


try:
    _config_file = pathlib.Path("backend.config.toml")
    _config = Config.model_validate(tomllib.load(_config_file.open("rb")))
except pydantic.ValidationError as error:
    sys.exit(str(error))

print(f"Loaded config from '{_config_file.name}'.")
CONFIG: Config = _config
