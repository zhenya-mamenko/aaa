# ruff: noqa: F403 F405
import pytest

from fastapi import HTTPException

from app.config import settings
from app.db.crud.utils import extract_create_stmts_objects
from app.db.sqlite import (
    execute_query,
    get_database_conn,
)
from app.services.services import *


def test_health_check(schema_files):
    result = health_check()
    assert result == "OK"

    execute_query("DROP VIEW IF EXISTS vw_assets;")
    with pytest.raises(HTTPException) as exc_info:
        health_check()
    assert exc_info.value.status_code == 500

    schema_views = extract_create_stmts_objects(f"{settings.database_schema_dir}views.sql", "VIEW")
    for view in schema_views:
        execute_query(f"DROP VIEW IF EXISTS {view};")
    with pytest.raises(HTTPException) as exc_info:
        health_check()
    assert exc_info.value.status_code == 500

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        health_check()
    assert exc_info.value.status_code == 500


def test_get_portfolio():
    result = get_portfolio()
    assert result
    row = result[0]
    assert 0 < row["structure_percentile"] < 1000
    assert 0 < row["total"]
    assert 0 <= row["current_percentile"] < 1000

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        get_portfolio()
    assert exc_info.value.status_code == 500
