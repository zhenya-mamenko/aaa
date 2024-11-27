from datetime import (
    date,
    datetime,
)
from typing import (
    Generic,
    TypeVar,
)

from pydantic import (
    BaseModel as _BaseModel,
    ConfigDict,
    field_validator,
)

from app.services import (
    get_assets,
    get_asset_categories,
    get_asset_classes,
    get_structures,
)


class BaseModel(_BaseModel):
    """
    Base model class for all models.

    This class serves as a base for all other models, providing common configurations
    and behaviors. It uses Pydantic's BaseModel as its foundation.
    """
    model_config = ConfigDict(extra='forbid')


T = TypeVar("T")

class ResponseModel(BaseModel, Generic[T]):
    """
    Generic response model.

    This model is used to standardize the structure of API responses that return
    a list of data items.

    Attributes:
        data (list[T]): The list of data items.
    """
    data: list[T]


__all__ = [
    "BaseModel",
    "ResponseModel",
    "date",
    "datetime",
    "field_validator",
    "get_asset_categories",
    "get_asset_classes",
    "get_assets",
    "get_structures",
]
