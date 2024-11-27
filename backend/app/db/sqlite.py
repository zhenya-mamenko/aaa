import sqlite3
import re

from app.config import settings

_database_path = settings.database_path
_database_conn = None


def connect(
    *, path: str | None = None, set_as_default: bool = False, force_connection: bool = False
) -> sqlite3.Connection:
    """
    Connect to the SQLite database. Use the default path if no path is provided.

    Args:
        path (str | None): The path to the database file. Defaults to None.
        set_as_default (bool): Whether to set this connection as the default. Defaults to False.

    Returns:
        sqlite3.Connection: The SQLite database connection.
    """

    conn = _database_conn
    if not conn or force_connection:
        conn = sqlite3.connect(path if path else _database_path)
    if set_as_default:
        set_database_conn(conn)
    return conn


def disconnect() -> None:
    """
    Disconnect from the default SQLite database.

    Returns:
        None
    """

    if _database_conn:
        _database_conn.close()
        set_database_conn(None)


def get_database_conn(*, auto_connect: bool = True) -> sqlite3.Connection:
    """
    Get the default SQLite database connection.

    Returns:
        sqlite3.Connection: The default SQLite database connection.
    """

    if not _database_conn and auto_connect:
        connect(set_as_default=True)
    return _database_conn


def set_database_conn(conn: sqlite3.Connection | None) -> None:
    """
    Set the default SQLite database connection.

    Args:
        conn (sqlite3.Connection | None): The SQLite database connection to set as default.

    Returns:
        None
    """

    global _database_conn
    _database_conn = conn


def read_query(
    query: str,
    /,
    *,
    parameters: tuple = (),
    conn: sqlite3.Connection | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> list[dict]:
    """
    Execute read query results on the SQLite database. Use the default connection if none is provided.

    Args:
        query (str): The SQL query to execute.
        parameters (tuple): The parameters to use in the query. Defaults to ().
        conn (sqlite3.Connection | None): The SQLite database connection to use. Defaults to None.
        limit (int | None): The maximum number of rows to return. Defaults to None.
        offset (int | None): The number of rows to skip. Defaults to None.

    Returns:
        list[dict]: The result of the query as a list of dictionaries.
    """

    if offset and not limit:
        raise ValueError("Offset cannot be used without limit.")

    query = re.sub(r";\s*$", "", query)
    if limit:
        query += f" LIMIT {limit}"
    if offset:
        query += f" OFFSET {offset}"
    query += ";"

    _conn = conn if conn else connect(set_as_default=False)
    _conn.row_factory = sqlite3.Row
    res = _conn.cursor().execute(query, parameters)
    result = [dict(row) for row in res.fetchall()]
    if not conn and not _database_conn: # pragma: no cover
        _conn.close()
    return result


def execute_query(
    query: str,
    /,
    *,
    parameters: tuple = (),
    conn: sqlite3.Connection | None = None,
) -> int:
    """
    Execute a DML query on the SQLite database. Use the default connection if none is provided.

    Args:
        query (str): The SQL query to execute.
        parameters (tuple): The parameters to use in the query. Defaults to ().
        conn (sqlite3.Connection | None): The SQLite database connection to use. Defaults to None.

    Returns:
        int: The number of rows affected by the query.
    """

    _conn = conn if conn else connect(set_as_default=False)
    cursor = _conn.cursor()
    cursor.execute("PRAGMA foreign_keys=1;")
    result = cursor.execute(query, parameters).rowcount
    _conn.commit()
    if not conn and not _database_conn: # pragma: no cover
        _conn.close()
    return result


__all__ = [
    "connect",
    "disconnect",
    "execute_query",
    "get_database_conn",
    "read_query",
    "set_database_conn",
]
