# ruff: noqa: F403 F405
import pytest

from fastapi import HTTPException

from app.db.sqlite import get_database_conn
from app.models import AssetClass
from app.services.classes import *


@pytest.fixture
def name1():
    return "Test 1"


@pytest.fixture
def name2():
    return "Test 2"


@pytest.fixture
def data_name():
    return "Cash"


@pytest.fixture
def data_id():
    return 4


@pytest.fixture
def asset_class(name1):
    return AssetClass(class_id=1, class_name=name1)


@pytest.fixture
def asset_class_no_id(name1):
    return AssetClass(class_name=name1)


def test_get_asset_class(data_name, data_id):
    asset_class = get_asset_class(data_id)
    assert asset_class
    assert asset_class["class_name"] == data_name

    with pytest.raises(HTTPException) as exc_info:
        get_asset_class(100)
    assert exc_info.value.status_code == 404

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        get_asset_class(data_id)
    assert exc_info.value.status_code == 500


def test_get_asset_classes(data_name, data_id):
    result = get_asset_classes()
    assert result
    assert len(result) == data_id
    asset_class = next(filter(lambda x: x["class_id"] == data_id, result))
    assert asset_class
    assert asset_class["class_name"] == data_name

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        get_asset_classes()
    assert exc_info.value.status_code == 500


def test_insert_asset_class(name1, name2, asset_class_no_id):
    result = insert_asset_class(asset_class_no_id)
    assert result
    assert result["class_name"] == name1

    with pytest.raises(HTTPException) as exc_info:
        insert_asset_class(asset_class_no_id)
    assert exc_info.value.status_code == 500

    get_database_conn().close()
    asset_class.class_name = name2
    with pytest.raises(HTTPException) as exc_info:
        insert_asset_class(asset_class_no_id)
    assert exc_info.value.status_code == 500


def test_update_asset_class(name1, asset_class):
    _asset_class = asset_class

    result = update_asset_class(asset_class)
    assert result
    assert result["class_name"] == name1

    _asset_class.class_id = 100
    with pytest.raises(HTTPException) as exc_info:
        update_asset_class(_asset_class)
    assert exc_info.value.status_code == 404

    _asset_class.class_id = 2
    with pytest.raises(HTTPException) as exc_info:
        update_asset_class(_asset_class)
    assert exc_info.value.status_code == 500

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        update_asset_class(asset_class)
    assert exc_info.value.status_code == 500


def test_delete_asset_class(name1, asset_class_no_id):
    with pytest.raises(HTTPException) as exc_info:
        delete_asset_class(1)
    assert exc_info.value.status_code == 500

    with pytest.raises(HTTPException) as exc_info:
        delete_asset_class(100)
    assert exc_info.value.status_code == 404

    result = insert_asset_class(asset_class_no_id)
    assert result
    id = result["class_id"]

    assert delete_asset_class(id)

    with pytest.raises(HTTPException) as exc_info:
        delete_asset_class(id)
    assert exc_info.value.status_code == 404

    result = insert_asset_class(asset_class_no_id)
    assert result
    id = result["class_id"]

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        delete_asset_class(id)
    assert exc_info.value.status_code == 500
