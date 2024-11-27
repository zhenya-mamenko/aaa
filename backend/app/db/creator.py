import csv
import os
import sqlite3
import sys

from argparse import ArgumentParser

from app.config import settings


def create_schema(cursor, schema_files: list) -> None:
    """
    Create the database schema from the provided schema files.

    Args:
        cursor: The database cursor.
        schema_files (list): List of schema file paths.

    Returns:
        None
    """

    for schema_file in schema_files:
        with open(schema_file, "r") as f:
            schema = f.read()
            cursor.executescript(schema)


def import_data(cursor, data_files: list, delimeter: ord) -> None:
    """
    Import data into the database from the provided data files.

    Args:
        cursor: The database cursor.
        data_files (list): List of data file paths.
        delimeter (ord): The delimiter used in the data files.

    Returns:
        None
    """

    for data_file in data_files:
        table = os.path.splitext(os.path.basename(data_file))[0]
        with open(data_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=chr(delimeter))
            if not reader.fieldnames: # pragma: no cover
                continue
            cols = ", ".join(reader.fieldnames)
            template = ", ".join(["?"] * len(reader.fieldnames))
            sql = f"INSERT INTO {table} ({cols}) VALUES ({template})"
            rows = [tuple(row.values()) for row in reader]
            cursor.executemany(sql, rows)


def parse_args(sys_args: list[str]) -> dict:
    """
    Parse command-line arguments.

    Args:
        sys_args (list[str]): List of command-line arguments.

    Returns:
        dict: Parsed arguments as a dictionary.
    """

    parser = ArgumentParser(
        prog="python -m app.db.creator",
        description=f"Create the schema for the {settings.app_name} database and import data if provided",
        epilog=f"See more on {settings.github_link}",
        allow_abbrev=False,
    )
    parser.add_argument("db_name", help="database filename", default=settings.database_path)
    parser.add_argument("-s", "--schema", nargs="*", help="filenames for db schema")
    parser.add_argument("-f", "--data", nargs="*", help="filenames for importing data")
    parser.add_argument("-d", type=ord, help="char for delimeter in data files", default="|")
    args = parser.parse_args(sys_args)

    return dict(db_name=args.db_name, schema=args.schema, data=args.data, delimeter=args.d)


def run(
    *,
    db_name: str | None = None,
    db_conn: sqlite3.Connection | None = None,
    schema: list = [],
    data: list = [],
    delimeter: ord = ord("|"),
) -> None:
    """
    Run the database creation and data import process.

    Args:
        db_name (str | None): The name of the database file.
        db_conn (sqlite3.Connection | None): The database connection.
        schema (list): List of schema file paths.
        data (list): List of data file paths.
        delimeter (ord): The delimiter used in the data files.

    Returns:
        None

    Raises:
        ValueError: If neither db_name nor db_conn is provided.
    """

    if not db_name and not db_conn:
        raise ValueError("Either db_name or db_conn must be provided")
    if not db_conn:
        conn = sqlite3.connect(db_name)
    else:
        conn = db_conn
    cursor = conn.cursor()

    if schema:
        create_schema(cursor, schema)
    if data:
        import_data(cursor, data, delimeter)

    conn.commit()
    if not db_conn:
        conn.close()


if __name__ == "__main__":
    args = parse_args(sys_args=sys.argv[1:])

    run(**args)
