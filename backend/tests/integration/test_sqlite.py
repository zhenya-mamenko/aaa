import pytest

from app.db.sqlite import (
    connect,
    disconnect,
    execute_query,
    get_database_conn,
    read_query,
    set_database_conn,
)

def test_read_query():
    result = read_query("SELECT * FROM classes;")
    assert result
    assert len(result) == 4

    result = read_query(
        "SELECT * FROM classes WHERE class_id = ?;",
        parameters=(2,)
    )
    assert result
    assert len(result) == 1
    assert result[0]["class_name"] == "Bonds"

    result = read_query(
        "SELECT * FROM classes ORDER BY class_id;",
        limit=2
    )
    assert len(result) == 2
    assert result[0]["class_name"] == "Stocks"
    assert result[1]["class_name"] == "Bonds"

    result = read_query(
        "SELECT * FROM classes ORDER BY class_id;",
        limit=3,
        offset=1
    )
    assert len(result) == 3
    assert result[0]["class_name"] == "Bonds"
    assert result[1]["class_name"] == "Alternates"
    assert result[2]["class_name"] == "Cash"

    with pytest.raises(ValueError):
        result = read_query(
            "SELECT * FROM classes ORDER BY class_id;",
            offset=3
        )

def test_execute_query():
    result = execute_query(
        "INSERT INTO classes (class_name) VALUES (?);",
        parameters=("Test",)
    )
    assert result == 1

    result = read_query(
        "SELECT * FROM classes WHERE class_id = ?;",
        parameters=(5,)
    )
    assert result
    assert len(result) == 1
    assert result[0]["class_name"] == "Test"

    result = execute_query(
        "UPDATE classes SET class_name = ? WHERE class_id = ?;",
        parameters=("Testing", 5)
    )
    assert result == 1

    result = read_query(
        "SELECT * FROM classes WHERE class_id = ?;",
        parameters=(5,)
    )
    assert result
    assert len(result) == 1
    assert result[0]["class_name"] == "Testing"

    result = execute_query(
        "DELETE FROM classes WHERE class_id = ?;",
        parameters=(5,)
    )
    assert result == 1

    result = read_query(
        "SELECT * FROM classes WHERE class_id = ?;",
        parameters=(5,)
    )
    assert not result


def test_connection():
    conn = connect(path=":memory:", set_as_default=True)
    assert conn
    assert get_database_conn() == conn
    disconnect()
    assert not get_database_conn(auto_connect=False)

    set_database_conn(None)
    assert not get_database_conn(auto_connect=False)
    conn = connect(path=":memory:", set_as_default=False)
    assert not get_database_conn(auto_connect=False)
    conn.close()

    disconnect()
    assert get_database_conn(auto_connect=True)
