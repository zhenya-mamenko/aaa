# ruff: noqa: F403 F405
import pytest

from fastapi import HTTPException

from app.db.sqlite import get_database_conn
from app.models import (
    Asset,
    AssetValue,
)
from app.services.assets import *


@pytest.fixture
def name1():
    return "Test 1"


@pytest.fixture
def name2():
    return "Test 2"


@pytest.fixture
def data_name():
    return "Etherium"


@pytest.fixture
def data_id():
    return 6


@pytest.fixture
def asset(name1):
    return Asset(asset_id=1, asset_name=name1, category_id=2, asset_ticker="TST1")


@pytest.fixture
def asset_no_id(name1):
    return Asset(asset_name=name1, category_id=2, asset_ticker="TST1")


@pytest.fixture
def asset_value(data_id):
    return AssetValue(asset_id=data_id, amount=10000)


def test_get_asset(data_name, data_id):
    asset = get_asset(data_id)
    assert asset
    assert asset["asset_name"] == data_name

    with pytest.raises(HTTPException) as exc_info:
        get_asset(100)
    assert exc_info.value.status_code == 404

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        get_asset(data_id)
    assert exc_info.value.status_code == 500


def test_get_assets(data_name, data_id):
    result = get_assets()
    assert result
    assert len(result) == 9
    asset = next(filter(lambda x: x["asset_id"] == data_id, result))
    assert asset
    assert asset["asset_name"] == data_name

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        get_assets()
    assert exc_info.value.status_code == 500


def test_get_assets_state(data_name, data_id):
    result = get_assets_state()
    assert len(result) == 6
    asset = next(filter(lambda x: x["asset_id"] == data_id, result))
    assert asset
    assert asset["asset_name"] == data_name

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        get_assets_state()
    assert exc_info.value.status_code == 500


def test_get_assets_values(data_id):
    result = get_assets_values()
    assert len(result) == 17
    assets = list(filter(lambda x: x["asset_id"] == data_id, result))
    assert assets
    assert len(assets) == 2

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        get_assets_values()
    assert exc_info.value.status_code == 500


def test_insert_asset(name1, name2, asset_no_id):
    result = insert_asset(asset_no_id)
    assert result
    assert result["asset_name"] == name1

    with pytest.raises(HTTPException) as exc_info:
        insert_asset(asset_no_id)
    assert exc_info.value.status_code == 500

    get_database_conn().close()
    asset.asset_name = name2
    with pytest.raises(HTTPException) as exc_info:
        insert_asset(asset_no_id)
    assert exc_info.value.status_code == 500


def test_update_asset(name1, asset):
    _asset = asset

    result = update_asset(asset)
    assert result
    assert result["asset_name"] == name1

    _asset.asset_id = 100
    with pytest.raises(HTTPException) as exc_info:
        update_asset(_asset)
    assert exc_info.value.status_code == 404

    _asset.asset_id = 2
    with pytest.raises(HTTPException) as exc_info:
        update_asset(_asset)
    assert exc_info.value.status_code == 500

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        update_asset(asset)
    assert exc_info.value.status_code == 500


def test_delete_asset(asset_no_id):
    with pytest.raises(HTTPException) as exc_info:
        delete_asset(1)
    assert exc_info.value.status_code == 500

    with pytest.raises(HTTPException) as exc_info:
        delete_asset(100)
    assert exc_info.value.status_code == 404

    result = insert_asset(asset_no_id)
    assert result
    id = result["asset_id"]

    assert delete_asset(id)

    with pytest.raises(HTTPException) as exc_info:
        delete_asset(id)
    assert exc_info.value.status_code == 404

    result = insert_asset(asset_no_id)
    assert result
    id = result["asset_id"]

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        delete_asset(id)
    assert exc_info.value.status_code == 500


def test_insert_asset_value(asset_value, data_id):
    result = insert_asset_value(asset_value)
    assert result
    assert result["asset_id"] == data_id

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        insert_asset_value(asset_value)
    assert exc_info.value.status_code == 500

