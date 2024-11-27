from app.models.base import (
    BaseModel,
    date,
    field_validator,
    get_asset_categories as _get_asset_categories,
    get_structures as _get_structures,
)


class Structure(BaseModel):
    """
    Model representing a structure of asset allocation.

    Attributes:
        structure_id (int | None): The ID of the structure.
        structure_date (str | date | None): The date of the structure (for reference only).
        structure_name (str): The name of the structure.
        is_current (bool): Whether the structure is currently in use.
    """
    structure_id: int | None = None
    structure_date: str | date | None = None
    structure_name: str
    is_current: bool

    @field_validator("structure_name")
    def name_must_not_be_blank(cls, v):
        if not v.strip():
            raise ValueError("structure_name must not be blank.")
        return v

    @field_validator("structure_date")
    def check_and_convert_date(cls, v):
        if v is None:
            return date.today()
        if isinstance(v, str):
            try:
                return date.fromisoformat(v)
            except ValueError:
                raise ValueError("structure_date must be a date string in the format YYYY-MM-DD.")
        return v


class StructureCategory(BaseModel):
    """
    Model representing a category in the structure of asset allocation.

    Attributes:
        structure_id (int): The ID of the structure.
        category_id (int): The ID of the category.
        percentile (int): The percentile of category's assets in the structure of asset allocation.
    """
    structure_id: int
    category_id: int
    percentile: int

    @field_validator("structure_id")
    def structure_id_must_exists(cls, v):
        ids = [c["structure_id"] for c in _get_structures()]
        if v not in ids:
            raise ValueError(f"structure_id={v} does not exist.")
        return v

    @field_validator("category_id")
    def category_id_must_exists(cls, v):
        ids = [c["category_id"] for c in _get_asset_categories()]
        if v not in ids:
            raise ValueError(f"category_id={v} does not exist.")
        return v

    @field_validator("percentile")
    def percentile_must_be_between_0_and_1000(cls, v):
        if not 0 < v < 1000:
            raise ValueError("percentile must be between 0 and 1000.")
        return v


class StructureCategoryResponse(BaseModel):
    """
    Response model for a structure category.

    Attributes:
        structure_id (int): The ID of the structure.
        category_id (int): The ID of the category.
        class_name (str): The name of the class.
        category_name (str): The name of the category.
        percentile (int): The percentile of category's assets in the structure of asset allocation.
        out_percentile (str): The output for the percentile.
    """
    structure_id: int
    category_id: int
    class_name: str
    category_name: str
    percentile: int
    out_percentile: str


__all__ = [
    "Structure",
    "StructureCategory",
    "StructureCategoryResponse",
]
