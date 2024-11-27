from app.models.base import (
    BaseModel,
    field_validator,
    get_asset_classes as _get_asset_classes,
)


class AssetCategory(BaseModel):
    """
    Model representing an asset category.

    Attributes:
        category_id (int | None): The ID of the asset category.
        class_id (int): The ID of the asset class.
        category_name (str): The name of the asset category.
    """
    category_id: int | None = None
    class_id: int
    category_name: str

    @field_validator("class_id")
    def class_id_must_exists(cls, v):
        ids = [c["class_id"] for c in _get_asset_classes()]
        if v not in ids:
            raise ValueError(f"class_id={v} does not exist.")
        return v

    @field_validator("category_name")
    def name_must_not_be_blank(cls, v):
        if not v.strip():
            raise ValueError("category_name must not be blank.")
        return v


class AssetCategoryResponse(BaseModel):
    """
    Response model for an asset category.

    Attributes:
        category_id (int): The ID of the category.
        class_id (int): The ID of the class.
        class_name (str): The name of the class.
        category_name (str): The name of the category.
    """
    category_id: int
    class_id: int
    class_name: str
    category_name: str
