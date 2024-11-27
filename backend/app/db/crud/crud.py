from app.db.sqlite import read_query as _read_query


def get_db_structure() -> tuple[list[dict], list[dict]]:
    """
    Retrieve the names of all tables and views in the database.

    Args:
        None

    Returns:
        tuple: A tuple containing two lists of dictionaries. The first list contains the names of tables,
               and the second list contains the names of views.

    Raises:
        Exception: If there is an error executing the query.
    """

    query = """
        SELECT
            name
        FROM sqlite_master
        WHERE type = 'table';
    """
    tables = [o["name"] for o in _read_query(query) if not o["name"].startswith("sqlite")]

    query = """
        SELECT
            name
        FROM sqlite_master
        WHERE type = 'view';
    """
    views = [o["name"] for o in _read_query(query) if not o["name"].startswith("sqlite")]

    return tables, views


def get_portfolio() -> list[dict]:
    """
    Retrieve the portfolio data from the database.

    Args:
        None

    Returns:
        list: A list of dictionaries containing portfolio data.

    Raises:
        Exception: If there is an error executing the query.
    """

    query = """
        SELECT
            p.category_id,
            c.class_name,
            c.category_name,
            p.structure_percentile,
            p.out_structure_percentile,
            p.amount,
            p.out_amount,
            p.total,
            p.out_total,
            p.current_percentile,
            p.out_current_percentile
        FROM vw_portfolio p
        INNER JOIN vw_categories c USING (category_id)
        WHERE structure_id = (
            SELECT
                structure_id
            FROM structures
            ORDER BY is_current DESC, structure_date DESC
            LIMIT 1
        )
        ORDER BY
            SUM(p.structure_percentile) OVER (PARTITION BY class_name) DESC,
            class_name,
            structure_percentile DESC,
            p.category_name
    """
    return _read_query(query)


__all__ = [
    "get_db_structure",
    "get_portfolio",
]
