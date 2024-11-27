from typing import TYPE_CHECKING

from fastapi import HTTPException

import app.db.crud as crud


if TYPE_CHECKING:
    from app.models import AssetClass


def get_asset_class(class_id: int) -> dict:
    """
    Retrieve a specific asset class by its ID.

    Args:
        class_id (int): The ID of the asset class to retrieve.

    Returns:
        dict: The asset class data.

    Raises:
        HTTPException: If an error occurs or the asset class is not found.
    """

    try:
        result = crud.get_asset_classes(class_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not result:
        raise HTTPException(status_code=404, detail=f"Class={class_id} not found")
    return result[0]


def get_asset_classes() -> list[dict]:
    """
    Retrieve all asset classes.

    Returns:
        list[dict]: A list of all asset classes.

    Raises:
        HTTPException: If an error occurs.
    """

    try:
        result = crud.get_asset_classes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return result


def insert_asset_class(asset_class: "AssetClass") -> dict:
    """
    Insert a new asset class.

    Args:
        asset_class (AssetClass): The asset class data to insert.

    Returns:
        dict: The inserted asset class data.

    Raises:
        HTTPException: If an error occurs.
    """

    try:
        result = crud.insert_asset_class(asset_class)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return result


def update_asset_class(asset_class: "AssetClass") -> dict:
    """
    Update an existing asset class.

    Args:
        asset_class (AssetClass): The asset class data to update.

    Returns:
        dict: The updated asset class data.

    Raises:
        HTTPException: If an error occurs or the asset class is not found.
    """

    try:
        result = crud.update_asset_class(asset_class)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not result:
        raise HTTPException(status_code=404, detail=f"Class={asset_class.class_id} not found")
    return result


def delete_asset_class(class_id: int) -> bool:
    """
    Delete an asset class by its ID.

    Args:
        class_id (int): The ID of the asset class to delete.

    Returns:
        bool: True if the asset class was deleted, False otherwise.

    Raises:
        HTTPException: If an error occurs or the asset class is not found.
    """

    try:
        result = crud.delete_asset_class(class_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not result:
        raise HTTPException(status_code=404, detail=f"Class={class_id} not found")
    return result


__all__ = [
    "delete_asset_class",
    "get_asset_class",
    "get_asset_classes",
    "insert_asset_class",
    "update_asset_class",
]
