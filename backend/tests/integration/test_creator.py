import os
import sqlite3
import tempfile

import pytest

from app.db.creator import create_schema, import_data, run


@pytest.fixture
def temp_db(database_path):
    conn = sqlite3.connect(database_path)
    yield conn
    conn.close()


@pytest.fixture
def temp_schema_file(schema_files):
    return schema_files[0]


@pytest.fixture
def temp_data_file(data_files):
    return data_files[0]


def test_create_schema(temp_db, temp_schema_file):
    cursor = temp_db.cursor()
    create_schema(cursor, [temp_schema_file])

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    assert ("classes",) in tables


def test_import_data(temp_db, temp_schema_file, temp_data_file):
    cursor = temp_db.cursor()
    create_schema(cursor, [temp_schema_file])
    import_data(cursor, [temp_data_file], ord("|"))

    cursor.execute("SELECT * FROM classes;")
    rows = cursor.fetchall()
    assert len(rows) == 4
    assert rows[0] == (1, "Stocks")
    assert rows[1] == (2, "Bonds")
    assert rows[2] == (3, "Alternates")
    assert rows[3] == (4, "Cash")


def test_run_with_db_name(temp_schema_file, temp_data_file):
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmpfile:
        db_name = tmpfile.name

    try:
        run(db_name=db_name, schema=[temp_schema_file], data=[temp_data_file], delimeter=ord("|"))

        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM classes;")
        rows = cursor.fetchall()

        assert len(rows) == 4
    finally:
        conn.close()
        os.remove(db_name)


def test_run_with_existing_conn(temp_db, temp_schema_file, temp_data_file):
    run(db_conn=temp_db, schema=[temp_schema_file], data=[temp_data_file], delimeter=ord("|"))

    cursor = temp_db.cursor()
    cursor.execute("SELECT * FROM classes;")
    rows = cursor.fetchall()

    assert len(rows) == 4
