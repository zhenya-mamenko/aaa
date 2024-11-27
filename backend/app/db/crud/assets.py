from typing import TYPE_CHECKING

from app.db.crud.utils import (
    delete_data_by_id,
    _get_database_conn,
    insert_data_from_model,
    update_data_from_model,
)
from app.db.sqlite import read_query as _read_query


if TYPE_CHECKING:
    from app.models import Asset, AssetValue


def get_assets(asset_id: int | None = None) -> list[dict]:
    """
    Retrieve assets from the database.

    Args:
        asset_id (int | None): The ID of the asset to retrieve. If None, retrieves all assets.

    Returns:
        list: A list of assets.
    """

    query = f"""
        SELECT
            asset_id,
            category_id,
            class_name,
            category_name,
            asset_name,
            asset_ticker
        FROM vw_assets
        {"WHERE asset_id = ?" if asset_id else ""}
        ORDER BY
            class_name,
            category_name,
            asset_name
    """
    return _read_query(query, parameters=(asset_id,) if asset_id else ())


def get_assets_state() -> list[dict]:
    """
    Retrieve the state of assets from the database.

    Returns:
        list: A list of asset states.
    """

    query = """
        SELECT
            asset_id,
            class_name,
            category_name,
            asset_name,
            asset_ticker,
            last,
            lag,
            first,
            last_lag_percent,
            last_first_percent,
            lag_first_percent,
            out_last,
            out_lag,
            out_first,
            out_last_lag_percent,
            out_last_first_percent,
            out_lag_first_percent
        FROM vw_assets_state
        ORDER BY
            class_name,
            category_name,
            asset_name
    """
    return _read_query(query)


def get_assets_values(value_id: int | None = None) -> list[dict]:
    """
    Retrieve the values of assets from the database.

    Args:
        value_id (int | None): The ID of the asset's value to retrieve. If None, retrieves all values.

    Returns:
        list: A list of assets values.
    """

    query = f"""
        SELECT
            asset_id,
            class_name,
            category_name,
            asset_name,
            asset_ticker,
            asset_value_datetime,
            amount,
            out_amount
        FROM vw_assets_values
        {"WHERE value_id = ?" if value_id else ""}
        ORDER BY
            asset_value_datetime DESC,
            class_name,
            category_name,
            asset_name
    """
    return _read_query(query, parameters=(value_id,) if value_id else ())


def insert_asset(asset: "Asset") -> dict:
    """
    Insert a new asset into the database.

    Args:
        asset (Asset): The asset model to insert.

    Returns:
        dict: The inserted asset.
    """

    id = insert_data_from_model(table_name="assets", id_field="asset_id", model=asset)
    return get_assets(id)[0]


def update_asset(asset: "Asset") -> dict | None:
    """
    Update an existing asset in the database.

    Args:
        asset (Asset): The asset model to update.

    Returns:
        dict | None: The updated asset if successful, otherwise None.
    """

    result = update_data_from_model(table_name="assets", id_field="asset_id", model=asset)
    return get_assets(asset.asset_id)[0] if result else None


def delete_asset(asset_id: int) -> bool:
    """
    Delete an asset from the database.

    Args:
        asset_id (int): The ID of the asset to delete.

    Returns:
        bool: True if the asset was deleted, otherwise False.
    """

    return delete_data_by_id(table_name="assets", id_field="asset_id", id_value=asset_id)


def insert_asset_value(asset_value: "AssetValue") -> dict:
    """
    Insert a new asset's value into the database.

    Args:
        asset+value (AssetValue): The asset's value model to insert.

    Returns:
        dict: The inserted asset's value.
    """

    with _get_database_conn() as conn:
        insert_data_from_model(table_name="assets_values", id_field=(), model=asset_value, auto_increment_id=False)
        query = "SELECT MAX(value_id) as value_id FROM assets_values;"
        value_id = _read_query(query, conn=conn)[0]["value_id"]
    return get_assets_values(value_id)[0]


__all__ = [
    "delete_asset",
    "get_assets",
    "get_assets_state",
    "get_assets_values",
    "insert_asset",
    "insert_asset_value",
    "update_asset",
]
