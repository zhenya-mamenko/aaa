from datetime import date

import pytest
from pydantic import ValidationError

from app.models import (
    AssetClass,
    AssetResponse,
    AssetsStateResponse,
    AssetsValuesResponse,
    ConfigEntry,
    PortfolioResponse,
    Structure,
    StructureCategoryResponse,
)


def test_asset_class():
    assert AssetClass(class_name="Stocks")

    asset_class = AssetClass(class_id=1, class_name="Stocks")
    assert asset_class.class_id == 1
    assert asset_class.class_name == "Stocks"
    assert asset_class.model_dump() == {
        "class_id": 1,
        "class_name": "Stocks",
    }

    assert asset_class.name_must_not_be_blank("Stocks") == "Stocks"
    with pytest.raises(ValueError) as exc_info:
        asset_class.name_must_not_be_blank("")
    assert exc_info.value.args[0] == "class_name must not be blank."

    with pytest.raises(ValidationError) as exc_info:
        asset_class = AssetClass(class_name="")
    assert exc_info.value.error_count() == 1
    assert exc_info.value.errors()[0]["msg"] == "Value error, class_name must not be blank."


def test_config_entry():
    config = ConfigEntry(config_name="currency", config_value={"symbol": "€", "position": "after"})
    assert config.config_name == "currency"
    assert config.config_value == dict(symbol="€", position="after")
    assert config.model_dump() == {"config_name": "currency", "config_value": {"symbol": "€", "position": "after"}}

    assert config.name_must_not_be_blank("currency") == "currency"
    with pytest.raises(ValueError) as exc_info:
        config.name_must_not_be_blank("")
    assert exc_info.value.args[0] == "config_name must not be blank."

    with pytest.raises(ValidationError) as exc_info:
        config = ConfigEntry(config_name="", config_value={"symbol": "€", "position": "after"})
    assert exc_info.value.error_count() == 1
    assert exc_info.value.errors()[0]["msg"] == "Value error, config_name must not be blank."

    assert config.check_and_convert_value('{"symbol": "€", "position": "after"}') == {
        "symbol": "€",
        "position": "after",
    }
    with pytest.raises(ValueError) as exc_info:
        config.check_and_convert_value("")
    assert exc_info.value.args[0] == "config_value must be a valid JSON."

    with pytest.raises(ValidationError) as exc_info:
        config = ConfigEntry(config_name="currency", config_value="")
    assert exc_info.value.error_count() == 1
    assert exc_info.value.errors()[0]["msg"] == "Value error, config_value must be a valid JSON."


def test_structure():
    assert Structure(structure_date="2024-11-15", structure_name="Portfolio", is_current=True)

    structure = Structure(structure_id=1, structure_date="2024-11-15", structure_name="Portfolio", is_current=True)
    assert structure
    assert structure.structure_id == 1
    assert structure.structure_date == date(2024, 11, 15)
    assert structure.structure_name == "Portfolio"
    assert structure.is_current
    assert structure.model_dump() == {
        "structure_id": 1,
        "structure_date": date(2024, 11, 15),
        "structure_name": "Portfolio",
        "is_current": True,
    }
    structure = Structure(structure_id=1, structure_date=date(2024, 11, 15), structure_name="Portfolio", is_current=True)
    assert structure

    structure = Structure(structure_id=1, structure_date=None, structure_name="Portfolio", is_current=True)
    assert structure

    assert structure.name_must_not_be_blank("Portfolio") == "Portfolio"
    with pytest.raises(ValueError) as exc_info:
        structure.name_must_not_be_blank("")
    assert exc_info.value.args[0] == "structure_name must not be blank."

    with pytest.raises(ValidationError) as exc_info:
        structure = Structure(structure_date="2024-11-15", structure_name="", is_current=True)
    assert exc_info.value.error_count() == 1
    assert exc_info.value.errors()[0]["msg"] == "Value error, structure_name must not be blank."

    assert structure.check_and_convert_date("2024-11-15") == date(2024, 11, 15)
    with pytest.raises(ValueError) as exc_info:
        structure.check_and_convert_date("2024/11/15")
    assert exc_info.value.args[0] == "structure_date must be a date string in the format YYYY-MM-DD."

    with pytest.raises(ValidationError) as exc_info:
        structure = Structure(structure_date="2024/11/15", structure_name="Portfolio", is_current=True)
    assert exc_info.value.error_count() == 1
    assert (
        exc_info.value.errors()[0]["msg"]
        == "Value error, structure_date must be a date string in the format YYYY-MM-DD."
    )


def test_structure_category_response():
    assert StructureCategoryResponse(
        structure_id=1, category_id=1, class_name="Stocks", category_name="Global stocks", percentile=500, out_percentile="50.0%"
    )

    with pytest.raises(ValidationError) as exc_info:
        StructureCategoryResponse(structure_id=1, category_id=1, class_name="Stocks", category_name="Global stocks", percentile=500)
    assert exc_info.value.error_count() == 1


def test_asset_response():
    assert AssetResponse(
        asset_id=1,
        category_id=1,
        class_name="Stocks",
        category_name="Global stocks",
        asset_name="Apple",
        asset_ticker="AAPL",
    )

    with pytest.raises(ValidationError) as exc_info:
        AssetResponse(
            category_id=1, class_name="Stocks", category_name="Global stocks", asset_name="Apple", asset_ticker="AAPL"
        )
    assert exc_info.value.error_count() == 1


def test_assets_state_response():
    assert AssetsStateResponse(
        asset_id=1,
        class_name="Stocks",
        category_name="Global stocks",
        asset_name="Apple",
        asset_ticker="AAPL",
        last=100,
        lag=90,
        first=80,
        last_lag_percent=10,
        last_first_percent=20,
        lag_first_percent=10,
        out_last="100",
        out_lag="90",
        out_first="80",
        out_last_lag_percent="10",
        out_last_first_percent="20",
        out_lag_first_percent="10",
    )

    with pytest.raises(ValidationError) as exc_info:
        AssetsStateResponse(
            class_name="Stocks",
            category_name="Global stocks",
            asset_name="Apple",
            asset_ticker="AAPL",
            last=100,
            lag=90,
            first=80,
            last_lag_percent=10,
            last_first_percent=20,
            lag_first_percent=10,
            out_last="100",
            out_lag="90",
            out_first="80",
            out_last_lag_percent="10",
            out_last_first_percent="20",
            out_lag_first_percent="10",
        )
    assert exc_info.value.error_count() == 1


def test_assets_values_response():
    assert AssetsValuesResponse(
        asset_id=1,
        class_name="Stocks",
        category_name="Global stocks",
        asset_name="Apple",
        asset_ticker="AAPL",
        asset_value_datetime="2024-11-15",
        amount=100,
        out_amount="100",
    )

    with pytest.raises(ValidationError) as exc_info:
        AssetsValuesResponse(
            class_name="Stocks",
            category_name="Global stocks",
            asset_name="Apple",
            asset_ticker="AAPL",
            asset_value_datetime="2024-11-15",
            amount=100,
            out_amount="100",
        )
    assert exc_info.value.error_count() == 1


def test_portfolio_response():
    assert PortfolioResponse(
        category_id=1,
        class_name="Stocks",
        category_name="Global stocks",
        structure_percentile=500,
        out_structure_percentile="50.0%",
        amount=100,
        out_amount="90",
        total=1000,
        out_total="900",
        current_percentile=50,
        out_current_percentile="5.0%",
    )

    with pytest.raises(ValidationError) as exc_info:
        PortfolioResponse(
            class_name="Stocks",
            category_name="Global stocks",
            structure_percentile=500,
            out_structure_percentile="50.0%",
            amount=100,
            out_amount="90",
            total=1000,
            out_total="900",
            current_percentile=50,
            out_current_percentile="5.0%",
        )
    assert exc_info.value.error_count() == 1