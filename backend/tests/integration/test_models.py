from datetime import datetime

import pytest
from pydantic import ValidationError

from app.models import (
    Asset,
    AssetCategory,
    AssetValue,
    StructureCategory,
)


def test_asset():
    assert Asset(category_id=1, asset_name="Bitcoin", asset_ticker="BTC")

    asset = Asset(asset_id=1, category_id=1, asset_name="Bitcoin", asset_ticker="BTC")
    assert asset.asset_id == 1
    assert asset.category_id == 1
    assert asset.asset_name == "Bitcoin"
    assert asset.asset_ticker == "BTC"
    assert asset.model_dump() == {
        "asset_id": 1,
        "category_id": 1,
        "asset_name": "Bitcoin",
        "asset_ticker": "BTC",
    }

    assert asset.name_must_not_be_blank("Bitcoin") == "Bitcoin"
    with pytest.raises(ValueError) as exc_info:
        asset.name_must_not_be_blank("")
    assert exc_info.value.args[0] == "asset_name must not be blank."

    with pytest.raises(ValidationError) as exc_info:
        asset = Asset(category_id=1, asset_name="", asset_ticker="BTC")
    assert exc_info.value.error_count() == 1
    assert exc_info.value.errors()[0]["msg"] == "Value error, asset_name must not be blank."

    assert asset.category_id_must_exists(1) == 1
    with pytest.raises(ValueError) as exc_info:
        asset.category_id_must_exists(10)
    assert exc_info.value.args[0] == "category_id=10 does not exist."

    with pytest.raises(ValidationError) as exc_info:
        asset = Asset(category_id=10, asset_name="Bitcoin", asset_ticker="BTC")
    assert exc_info.value.error_count() == 1
    assert exc_info.value.errors()[0]["msg"] == "Value error, category_id=10 does not exist."

    assert asset.asset_ticker_must_not_be_more_20_chars("BTC") == "BTC"
    with pytest.raises(ValueError) as exc_info:
        asset.asset_ticker_must_not_be_more_20_chars("BTC" * 10)
    assert exc_info.value.args[0] == "asset_ticker must not be more 20 chars."

    with pytest.raises(ValidationError) as exc_info:
        asset = Asset(category_id=1, asset_name="Bitcoin", asset_ticker="BTC" * 10)
    assert exc_info.value.error_count() == 1
    assert exc_info.value.errors()[0]["msg"] == "Value error, asset_ticker must not be more 20 chars."


def test_asset_category():
    asset_category = AssetCategory(category_id=1, class_id=1, category_name="Global stocks")
    assert asset_category.category_id == 1
    assert asset_category.class_id == 1
    assert asset_category.category_name == "Global stocks"
    assert asset_category.model_dump() == {
        "category_id": 1,
        "class_id": 1,
        "category_name": "Global stocks",
    }

    assert asset_category.name_must_not_be_blank("Global stocks") == "Global stocks"
    with pytest.raises(ValueError) as exc_info:
        asset_category.name_must_not_be_blank("")
    assert exc_info.value.args[0] == "category_name must not be blank."

    with pytest.raises(ValidationError) as exc_info:
        asset_category = AssetCategory(class_id=1, category_name="")
    assert exc_info.value.error_count() == 1
    assert exc_info.value.errors()[0]["msg"] == "Value error, category_name must not be blank."

    assert asset_category.class_id_must_exists(1) == 1
    with pytest.raises(ValueError) as exc_info:
        asset_category.class_id_must_exists(10)
    assert exc_info.value.args[0] == "class_id=10 does not exist."

    with pytest.raises(ValidationError) as exc_info:
        asset_category = AssetCategory(class_id=10, category_name="Global stocks")
    assert exc_info.value.error_count() == 1
    assert exc_info.value.errors()[0]["msg"] == "Value error, class_id=10 does not exist."


def test_asset_value():
    asset_value = AssetValue(value_datetime="2024-11-15 23:55:00", asset_id=1, amount=100000)
    assert asset_value
    assert asset_value.value_datetime == datetime(2024, 11, 15, 23, 55)
    assert asset_value.asset_id == 1
    assert asset_value.amount == 100000
    assert asset_value.model_dump() == {
        "value_datetime": datetime(2024, 11, 15, 23, 55),
        "asset_id": 1,
        "amount": 100000,
    }
    asset_value = AssetValue(value_datetime=datetime(2024, 11, 15, 23, 55), asset_id=1, amount=100000)
    assert asset_value

    asset_value = AssetValue(value_datetime=None, asset_id=1, amount=100000)
    assert asset_value

    asset_value = AssetValue( asset_id=1, amount=100000)
    assert asset_value

    with pytest.raises(ValidationError) as exc_info:
        assert AssetValue(value_datetime=datetime(2024, 11, 15, 23, 55), amount=100000)
    assert exc_info.value.error_count() == 1

    assert asset_value.asset_id_must_exists(1) == 1
    with pytest.raises(ValueError) as exc_info:
        asset_value.asset_id_must_exists(10)
    assert exc_info.value.args[0] == "asset_id=10 does not exist."

    with pytest.raises(ValidationError) as exc_info:
        asset_value = AssetValue(value_datetime="2024-11-15 23:55", asset_id=10, amount=100000)
    assert exc_info.value.error_count() == 1
    assert exc_info.value.errors()[0]["msg"] == "Value error, asset_id=10 does not exist."

    assert asset_value.check_and_convert_datetime("2024-11-15 23:55:15") == datetime(2024, 11, 15, 23, 55, 15)
    with pytest.raises(ValueError) as exc_info:
        asset_value.check_and_convert_datetime("2024/11/15 23:55:15")
    assert exc_info.value.args[0] == "value_datetime must be a datetime string in the iso format."

    with pytest.raises(ValidationError) as exc_info:
        asset_value = AssetValue(value_datetime="2024/11/15 23:15", asset_id=1, amount=100000)
    assert exc_info.value.error_count() == 1
    assert exc_info.value.errors()[0]["msg"] == "Value error, value_datetime must be a datetime string in the iso format."

    assert asset_value.amount_must_be_positive_or_zero(100000) == 100000
    with pytest.raises(ValueError) as exc_info:
        asset_value.amount_must_be_positive_or_zero(-1)
    assert exc_info.value.args[0] == "amount must be positive or zero."

    with pytest.raises(ValidationError) as exc_info:
        asset_value = AssetValue(value_datetime="2024-11-15 23:55:15", asset_id=1, amount=-1)
    assert exc_info.value.error_count() == 1
    assert exc_info.value.errors()[0]["msg"] == "Value error, amount must be positive or zero."


def test_structure_categories():
    structure_category = StructureCategory(structure_id=1, category_id=1, percentile=500)
    assert structure_category
    assert structure_category.structure_id == 1
    assert structure_category.category_id == 1
    assert structure_category.percentile == 500
    assert structure_category.model_dump() == {
        "structure_id": 1,
        "category_id": 1,
        "percentile": 500,
    }
    with pytest.raises(ValidationError) as exc_info:
        StructureCategory(category_id=1, percentile=500)
    assert exc_info.value.error_count() == 1

    assert structure_category.percentile_must_be_between_0_and_1000(500) == 500
    with pytest.raises(ValueError) as exc_info:
        structure_category.percentile_must_be_between_0_and_1000(-1)
    assert exc_info.value.args[0] == "percentile must be between 0 and 1000."

    with pytest.raises(ValidationError) as exc_info:
        structure_category = StructureCategory(structure_id=1, category_id=1, percentile=1000)
    assert exc_info.value.error_count() == 1
    assert exc_info.value.errors()[0]["msg"] == "Value error, percentile must be between 0 and 1000."

    assert structure_category.category_id_must_exists(1) == 1
    with pytest.raises(ValueError) as exc_info:
        structure_category.category_id_must_exists(10)
    assert exc_info.value.args[0] == "category_id=10 does not exist."

    with pytest.raises(ValidationError) as exc_info:
        structure_category = StructureCategory(structure_id=1, category_id=10, percentile=500)
    assert exc_info.value.error_count() == 1
    assert exc_info.value.errors()[0]["msg"] == "Value error, category_id=10 does not exist."

    assert structure_category.structure_id_must_exists(1) == 1
    with pytest.raises(ValueError) as exc_info:
        structure_category.structure_id_must_exists(10)
    assert exc_info.value.args[0] == "structure_id=10 does not exist."

    with pytest.raises(ValidationError) as exc_info:
        structure_category = StructureCategory(structure_id=10, category_id=1, percentile=500)
    assert exc_info.value.error_count() == 1
    assert exc_info.value.errors()[0]["msg"] == "Value error, structure_id=10 does not exist."
