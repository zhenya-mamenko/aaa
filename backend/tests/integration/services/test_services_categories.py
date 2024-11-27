# ruff: noqa: F403 F405
import pytest
from fastapi import HTTPException

from app.db.sqlite import get_database_conn
from app.models import AssetCategory
from app.services.categories import *


@pytest.fixture
def name1():
    return "Test 1"


@pytest.fixture
def name2():
    return "Test 2"


@pytest.fixture
def data_name():
    return "Cryptocurrency"


@pytest.fixture
def data_id():
    return 6


@pytest.fixture
def asset_category(name1):
    return AssetCategory(category_id=1, class_id=2, category_name=name1)


@pytest.fixture
def asset_category_no_id(name1):
    return AssetCategory(class_id=2, category_name=name1)


def test_get_asset_categories(data_name, data_id):
    result = get_asset_categories()
    assert result
    assert len(result) == 7
    category = next(filter(lambda x: x["category_id"] == data_id, result))
    assert category
    assert category["category_name"] == data_name

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        get_asset_categories()
    assert exc_info.value.status_code == 500


def test_get_asset_category(data_name, data_id):
    asset_category = get_asset_category(data_id)
    assert asset_category
    assert asset_category["category_name"] == data_name

    with pytest.raises(HTTPException) as exc_info:
        get_asset_category(100)
    assert exc_info.value.status_code == 404

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        get_asset_category(data_id)
    assert exc_info.value.status_code == 500


def test_insert_asset_category(asset_category_no_id, name1, name2):
    result = insert_asset_category(asset_category_no_id)
    assert result
    assert result["category_name"] == name1

    with pytest.raises(HTTPException) as exc_info:
        insert_asset_category(asset_category_no_id)
    assert exc_info.value.status_code == 500

    get_database_conn().close()
    asset_category.category_name = name2
    with pytest.raises(HTTPException) as exc_info:
        insert_asset_category(asset_category_no_id)
    assert exc_info.value.status_code == 500


def test_update_asset_category(asset_category, name1):
    _asset_category = asset_category

    result = update_asset_category(_asset_category)
    assert result
    assert result["category_name"] == name1

    _asset_category.category_id = 100
    with pytest.raises(HTTPException) as exc_info:
        update_asset_category(_asset_category)
    assert exc_info.value.status_code == 404

    _asset_category.category_id = 2
    with pytest.raises(HTTPException) as exc_info:
        update_asset_category(_asset_category)
    assert exc_info.value.status_code == 500

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        update_asset_category(asset_category)
    assert exc_info.value.status_code == 500


def test_delete_asset_category(asset_category_no_id):
    with pytest.raises(HTTPException) as exc_info:
        delete_asset_category(1)
    assert exc_info.value.status_code == 500

    with pytest.raises(HTTPException) as exc_info:
        delete_asset_category(100)
    assert exc_info.value.status_code == 404

    result = insert_asset_category(asset_category_no_id)
    assert result
    id = result["category_id"]

    delete_asset_category(id)
    with pytest.raises(HTTPException) as exc_info:
        delete_asset_category(id)
    assert exc_info.value.status_code == 404

    result = insert_asset_category(asset_category_no_id)
    assert result
    id = result["class_id"]

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        delete_asset_category(id)
    assert exc_info.value.status_code == 500
