import json

from app.models.base import (
    BaseModel,
    field_validator,
)


class ConfigEntry(BaseModel):
    """
    Model representing a configuration entry.

    Attributes:
        config_name (str): The name of the configuration entry.
        config_value (dict | str): The value of the configuration entry.
    """
    config_name: str | None = None
    config_value: dict | str

    @field_validator("config_name")
    def name_must_not_be_blank(cls, v):
        if not v.strip():
            raise ValueError("config_name must not be blank.")
        return v

    @field_validator("config_value")
    def check_and_convert_value(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except ValueError:
                raise ValueError("config_value must be a valid JSON.")
        return v


__all__ = [
    "ConfigEntry",
]
