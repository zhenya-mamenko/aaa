from app.models.base import (
    BaseModel,
    field_validator,
)


class AssetClass(BaseModel):
    """
    Model representing an asset class.

    Attributes:
        class_id (int | None): The ID of the asset class.
        class_name (str): The name of the asset class.
    """
    class_id: int | None = None
    class_name: str

    @field_validator("class_name")
    def name_must_not_be_blank(cls, v):
        if not v.strip():
            raise ValueError("class_name must not be blank.")
        return v


class AssetClassResponse(BaseModel):
    """
    Response model for an asset class.

    Attributes:
        class_id (int): The ID of the class.
        class_name (str): The name of the class.
    """
    class_id: int
    class_name: str


__all__ = [
    "AssetClass",
    "AssetClassResponse",
]
