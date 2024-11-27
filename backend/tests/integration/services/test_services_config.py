import pytest

from fastapi import HTTPException

from app.db.sqlite import get_database_conn
from app.models import ConfigEntry
from app.services import (
    delete_config,
    get_config,
    get_config_value,
    insert_config,
    update_config,
)


@pytest.fixture
def name1():
    return "Test 1"


@pytest.fixture
def name2():
    return "Test 2"


@pytest.fixture
def config_value():
    return dict(symbol="$", position="before")


@pytest.fixture
def config_name():
    return "currency"


@pytest.fixture
def config_entry(name1, config_value):
    return ConfigEntry(config_name=name1, config_value=config_value)


def test_get_config(config_name):
    result = get_config()
    assert len(result) == 1
    config = next(filter(lambda x: x["config_name"] == config_name, result))
    assert config

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        get_config()
    assert exc_info.value.status_code == 500

def test_get_config_value(config_name, name1):
    config_entry = get_config_value(config_name)
    assert config_entry

    with pytest.raises(HTTPException) as exc_info:
        get_config_value(name1)
    assert exc_info.value.status_code == 404

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        get_config_value(config_name)
    assert exc_info.value.status_code == 500


def test_insert_config(name1, name2, config_entry, config_value):
    result = insert_config(config_entry)
    assert result
    result = ConfigEntry(**result)
    assert result.config_name == name1
    assert result.config_value == config_value

    with pytest.raises(HTTPException) as exc_info:
        insert_config(config_entry)
    assert exc_info.value.status_code == 500

    get_database_conn().close()
    config_entry.config_name = name2
    with pytest.raises(HTTPException) as exc_info:
        insert_config(config_entry)
    assert exc_info.value.status_code == 500


def test_update_config(config_name, name1, name2, config_entry, config_value):
    config_entry.config_name = config_name
    result = update_config(config_entry)
    result = ConfigEntry(**result)
    assert result.config_value == config_value

    config_entry.config_name = name1
    with pytest.raises(HTTPException) as exc_info:
        update_config(config_entry)
    assert exc_info.value.status_code == 404

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        update_config(config_entry)
    assert exc_info.value.status_code == 500


def test_delete_config(name1, config_name, config_entry):
    with pytest.raises(HTTPException) as exc_info:
        delete_config(name1)
    assert exc_info.value.status_code == 404

    result = insert_config(config_entry)
    assert result

    assert delete_config(name1)

    with pytest.raises(HTTPException) as exc_info:
        delete_config(name1)
    assert exc_info.value.status_code == 404

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        delete_config(config_name)
    assert exc_info.value.status_code == 500
