from typing import TYPE_CHECKING

from app.db.crud.utils import (
    delete_data_by_id,
    insert_data_from_model,
    update_data_from_model,
)
from app.db.sqlite import read_query as _read_query


if TYPE_CHECKING:
    from app.models import AssetCategory


def get_asset_categories(category_id: int | None = None) -> list[dict]:
    """
    Retrieve asset categories from the database.

    Args:
        category_id (int | None): The ID of the category to retrieve. If None, retrieves all categories.

    Returns:
        list[dict]: A list of dictionaries representing the asset categories.
    """

    query = f"""
        SELECT
            category_id,
            class_id,
            class_name,
            category_name
        FROM vw_categories
        {"WHERE category_id = ?" if category_id else ""}
        ORDER BY
            category_name
    """
    return _read_query(query, parameters=(category_id,) if category_id else ())


def insert_asset_category(asset_category: "AssetCategory") -> dict:
    """
    Insert a new asset category into the database.

    Args:
        asset_category (AssetCategory): The asset category model to insert.

    Returns:
        dict: A dictionary representing the inserted asset category.
    """

    id = insert_data_from_model(table_name="categories", id_field="category_id", model=asset_category)
    return get_asset_categories(id)[0]


def update_asset_category(asset_category: "AssetCategory") -> dict | None:
    """
    Update an existing asset category in the database.

    Args:
        asset_category (AssetCategory): The asset category model to update.

    Returns:
        dict | None: A dictionary representing the updated asset category, or None if the update failed.
    """

    result = update_data_from_model(table_name="categories", id_field="category_id", model=asset_category)
    return get_asset_categories(asset_category.category_id)[0] if result else None


def delete_asset_category(category_id: int) -> bool:
    """
    Delete an asset category from the database.

    Args:
        category_id (int): The ID of the category to delete.

    Returns:
        bool: True if the deletion was successful, False otherwise.
    """

    return delete_data_by_id(table_name="categories", id_field="category_id", id_value=category_id)


__all__ = [
    "delete_asset_category",
    "get_asset_categories",
    "insert_asset_category",
    "update_asset_category",
]
