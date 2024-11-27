from typing import TYPE_CHECKING

from fastapi import HTTPException

import app.db.crud as crud

if TYPE_CHECKING:
    from app.models import AssetCategory


def get_asset_categories() -> list[dict]:
    """
    Retrieve all asset categories.

    Returns:
        List of asset categories.
    """

    try:
        result = crud.get_asset_categories()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return result


def get_asset_category(category_id: int) -> dict:
    """
    Retrieve a specific asset category by its ID.

    Args:
        category_id (int): The ID of the asset category.

    Returns:
        The asset category with the specified ID.

    Raises:
        HTTPException: If the category is not found or an error occurs.
    """

    try:
        result = crud.get_asset_categories(category_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not result:
        raise HTTPException(status_code=404, detail=f"Category={category_id} not found")
    return result[0]


def insert_asset_category(asset_category: "AssetCategory") -> dict:
    """
    Insert a new asset category.

    Args:
        asset_category (AssetCategory): The asset category to insert.

    Returns:
        The inserted asset category.

    Raises:
        HTTPException: If an error occurs during insertion.
    """

    try:
        result = crud.insert_asset_category(asset_category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return result


def update_asset_category(asset_category: "AssetCategory") -> dict:
    """
    Update an existing asset category.

    Args:
        asset_category (AssetCategory): The asset category to update.

    Returns:
        The updated asset category.

    Raises:
        HTTPException: If the category is not found or an error occurs during update.
    """

    try:
        result = crud.update_asset_category(asset_category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not result:
        raise HTTPException(status_code=404, detail=f"Category={asset_category.category_id} not found")
    return result


def delete_asset_category(category_id: int) -> bool:
    """
    Delete an asset category by its ID.

    Args:
        category_id (int): The ID of the asset category to delete.

    Returns:
        bool: True if the deletion was successful, False otherwise.

    Raises:
        HTTPException: If the category is not found or an error occurs during deletion.
    """

    try:
        result = crud.delete_asset_category(category_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not result:
        raise HTTPException(status_code=404, detail=f"Category={category_id} not found")
    return result


__all__ = [
    "delete_asset_category",
    "get_asset_categories",
    "get_asset_category",
    "insert_asset_category",
    "update_asset_category",
]
