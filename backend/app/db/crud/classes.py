from typing import TYPE_CHECKING

from app.db.crud.utils import (
    delete_data_by_id,
    insert_data_from_model,
    update_data_from_model,
)
from app.db.sqlite import read_query as _read_query


if TYPE_CHECKING:
    from app.models import AssetClass


def get_asset_classes(class_id: int | None = None) -> list[dict]:
    """
    Retrieve asset classes from the database.

    Args:
        class_id (int | None): The ID of the asset class to retrieve. If None, retrieves all asset classes.

    Returns:
        list: A list of asset classes.
    """

    query = f"""
        SELECT
            class_id,
            class_name
        FROM classes
        {"WHERE class_id = ?" if class_id else ""}
        ORDER BY
            class_name
    """

    return _read_query(query, parameters=(class_id,) if class_id else ())


def insert_asset_class(asset_class: "AssetClass") -> dict:
    """
    Insert a new asset class into the database.

    Args:
        asset_class (AssetClass): The asset class model to insert.

    Returns:
        dict: The inserted asset class.
    """

    id = insert_data_from_model(table_name="classes", id_field="class_id", model=asset_class)
    return get_asset_classes(id)[0]


def update_asset_class(asset_class: "AssetClass") -> dict | None:
    """
    Update an existing asset class in the database.

    Args:
        asset_class (AssetClass): The asset class model to update.

    Returns:
        dict | None: The updated asset class if successful, otherwise None.
    """

    result = update_data_from_model(table_name="classes", id_field="class_id", model=asset_class)
    return get_asset_classes(asset_class.class_id)[0] if result else None


def delete_asset_class(class_id: int) -> bool:
    """
    Delete an asset class from the database.

    Args:
        class_id (int): The ID of the asset class to delete.

    Returns:
        bool: True if the deletion was successful, otherwise False.
    """

    return delete_data_by_id(table_name="classes", id_field="class_id", id_value=class_id)


__all__ = [
    "delete_asset_class",
    "get_asset_classes",
    "insert_asset_class",
    "update_asset_class",
]
