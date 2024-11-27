from app.models.base import (
    BaseModel,
    datetime,
    field_validator,
    get_asset_categories as _get_asset_categories,
    get_assets as _get_assets,
)


class Asset(BaseModel):
    """
    Model representing an asset.

    Attributes:
        asset_id (int | None): The ID of the asset.
        category_id (int): The ID of the asset category.
        asset_name (str): The name of the asset.
        asset_ticker (str): The asset_ticker of the asset.
    """
    asset_id: int | None = None
    category_id: int
    asset_name: str
    asset_ticker: str

    @field_validator("category_id")
    def category_id_must_exists(cls, v):
        ids = [c["category_id"] for c in _get_asset_categories()]
        if v not in ids:
            raise ValueError(f"category_id={v} does not exist.")
        return v

    @field_validator("asset_name")
    def name_must_not_be_blank(cls, v):
        if not v.strip():
            raise ValueError("asset_name must not be blank.")
        return v

    @field_validator("asset_ticker")
    def asset_ticker_must_not_be_more_20_chars(cls, v):
        if len(v) > 20:
            raise ValueError("asset_ticker must not be more 20 chars.")
        return v


class AssetValue(BaseModel):
    """
    Model representing the value of an asset.

    Attributes:
        value_datetime (str | datetime): The datetime of taking the asset value.
        asset_id (int): The ID of the asset.
        amount (int): The amount of the asset value in cents.
    """
    value_datetime: str | datetime | None = None
    asset_id: int
    amount: int

    @field_validator("value_datetime")
    def check_and_convert_datetime(cls, v):
        if v is None:
            return datetime.now()
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v)
            except ValueError:
                raise ValueError("value_datetime must be a datetime string in the iso format.")
        return v

    @field_validator("amount")
    def amount_must_be_positive_or_zero(cls, v):
        if v < 0:
            raise ValueError("amount must be positive or zero.")
        return v

    @field_validator("asset_id")
    def asset_id_must_exists(cls, v):
        ids = [c["asset_id"] for c in _get_assets()]
        if v not in ids:
            raise ValueError(f"asset_id={v} does not exist.")
        return v


class AssetResponse(BaseModel):
    """
    Response model for an asset.

    Attributes:
        asset_id (int): The ID of the asset.
        category_id (int): The ID of the category.
        class_name (str): The name of the class.
        category_name (str): The name of the category.
        asset_name (str): The name of the asset.
        asset_ticker (str): The asset_ticker of the asset.
    """
    asset_id: int
    category_id: int
    class_name: str
    category_name: str
    asset_name: str
    asset_ticker: str


class AssetsStateResponse(BaseModel):
    """
    Response model for the state of assets.

    Attributes:
        asset_id (int): The ID of the asset.
        class_name (str): The name of the class.
        category_name (str): The name of the category.
        asset_name (str): The name of the asset.
        asset_ticker (str): The asset_ticker of the asset.
        last (int): The last amount of the asset value in cents.
        lag (int): The lag (previous of the last) amount of the asset value in cents.
        first (int): The first amount of the asset value in cents.
        last_lag_percent (float): The percentage change from last to lag.
        last_first_percent (float): The percentage change from last to first.
        lag_first_percent (float): The percentage change from lag to first.
        out_last (str): The output for the last value.
        out_lag (str): The output for the lag value.
        out_first (str): The output for the first value.
        out_last_lag_percent (str): The output for the percentage change from last to lag.
        out_last_first_percent (str): The output for the percentage change from last to first.
        out_lag_first_percent (str): The output for the percentage change from lag to first.
    """
    asset_id: int
    class_name: str
    category_name: str
    asset_name: str
    asset_ticker: str
    last: int
    lag: int
    first: int
    last_lag_percent: float
    last_first_percent: float
    lag_first_percent: float
    out_last: str
    out_lag: str
    out_first: str
    out_last_lag_percent: str
    out_last_first_percent: str
    out_lag_first_percent: str


class AssetsValuesResponse(BaseModel):
    """
    Response model for the values of assets.

    Attributes:
        asset_id (int): The ID of the asset.
        class_name (str): The name of the class.
        category_name (str): The name of the category.
        asset_name (str): The name of the asset.
        asset_ticker (str): The asset_ticker of the asset.
        asset_value_datetime (str): The datetime of taking the asset value.
        amount (int): The amount of the asset value in cents.
        out_amount (str): The output for the amount.
    """
    asset_id: int
    class_name: str
    category_name: str
    asset_name: str
    asset_ticker: str
    asset_value_datetime: str
    amount: int
    out_amount: str


__all__ = [
    "Asset",
    "AssetResponse",
    "AssetValue",
    "AssetsStateResponse",
    "AssetsValuesResponse",
]
