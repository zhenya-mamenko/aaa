from fastapi import HTTPException

import app.db.crud as crud

from app.config import settings
from app.db.crud.utils import extract_create_stmts_objects


def health_check() -> str:
    """
    Perform a health check.

    Args:
        None

    Returns:
        str: The health check status.

    Raises:
        HTTPException: If there is an error performing the health check.
    """

    try:
        tables, views = crud.get_db_structure()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not tables or not views:
        raise HTTPException(status_code=500, detail="Database is empty.")

    schema_tables = extract_create_stmts_objects(f"{settings.database_schema_dir}schema.sql", "TABLE")
    schema_views = extract_create_stmts_objects(f"{settings.database_schema_dir}views.sql", "VIEW")

    if (set(tables) ^ set(schema_tables) != set()) or (set(views) ^ set(schema_views) != set()):
        raise HTTPException(status_code=500, detail="Database schema does not match the expected schema.")

    return "OK"


def get_portfolio():
    """
    Retrieve the portfolio data.

    Args:
        None

    Returns:
        dict: The portfolio data retrieved from the database.

    Raises:
        HTTPException: If there is an error retrieving the portfolio data.
    """

    try:
        result = crud.get_portfolio()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return result


__all__ = [
    "health_check",
    "get_portfolio",
]
