import pytest

from app.config import settings
from app.db.creator import run as _create_db
from app.db.sqlite import (
    connect as _db_connect,
    disconnect as _db_disconnect,
)


@pytest.fixture
def schema_files():
    files = [
        "schema.sql",
        "views.sql",
    ]
    return [f"{settings.database_schema_dir}{f}" for f in files]


@pytest.fixture
def data_files():
    files = [
        "classes.csv",
        "categories.csv",
        "assets.csv",
        "structures.csv",
        "structure_categories.csv",
        "assets_values.csv",
        "config.csv",
    ]
    return [f"{settings.database_import_data_dir}{f}" for f in files]


@pytest.fixture
def database_path():
    return ":memory:" if settings.environment != "test" or settings.database_path == "" else settings.database_path


@pytest.fixture(autouse=True)
def db(database_path, schema_files, data_files):
    conn = _db_connect(path=database_path, set_as_default=True)
    _create_db(db_conn=conn, schema=schema_files, data=data_files, delimeter=ord("|"))
    yield
    _db_disconnect()
