from typing import TYPE_CHECKING

from fastapi import HTTPException

import app.db.crud as crud


if TYPE_CHECKING:
    from app.models import Asset, AssetValue


def get_asset(asset_id: int) -> dict:
    """
    Retrieve a single asset by its ID.

    Args:
        asset_id (int): The ID of the asset to retrieve.

    Returns:
        dict: The asset data.

    Raises:
        HTTPException: If an error occurs or the asset is not found.
    """

    try:
        result = crud.get_assets(asset_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not result:
        raise HTTPException(status_code=404, detail=f"Asset={asset_id} not found")
    return result[0]


def get_assets() -> list[dict]:
    """
    Retrieve all assets.

    Returns:
        list[dict]: A list of all assets.

    Raises:
        HTTPException: If an error occurs.
    """

    try:
        result = crud.get_assets()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return result


def get_assets_state() -> list[dict]:
    """
    Retrieve the state of all assets.

    Returns:
        list[dict]: A list of asset states.

    Raises:
        HTTPException: If an error occurs.
    """

    try:
        result = crud.get_assets_state()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return result


def get_assets_values() -> list[dict]:
    """
    Retrieve the values of all assets.

    Returns:
        list[dict]: A list of asset values.

    Raises:
        HTTPException: If an error occurs.
    """

    try:
        result = crud.get_assets_values()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return result


def insert_asset(asset: "Asset") -> dict:
    """
    Insert a new asset.

    Args:
        asset (Asset): The asset to insert.

    Returns:
        dict: The inserted asset data.

    Raises:
        HTTPException: If an error occurs.
    """

    try:
        result = crud.insert_asset(asset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return result


def update_asset(asset: "Asset") -> dict:
    """
    Update an existing asset.

    Args:
        asset (Asset): The asset to update.

    Returns:
        dict: The updated asset data.

    Raises:
        HTTPException: If an error occurs or the asset is not found.
    """

    try:
        result = crud.update_asset(asset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not result:
        raise HTTPException(status_code=404, detail=f"Asset={asset.asset_id} not found")
    return result


def delete_asset(asset_id: int) -> bool:
    """
    Delete an asset by its ID.

    Args:
        asset_id (int): The ID of the asset to delete.

    Returns:
        bool: True if the asset was deleted, False otherwise.

    Raises:
        HTTPException: If an error occurs or the asset is not found.
    """

    try:
        result = crud.delete_asset(asset_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not result:
        raise HTTPException(status_code=404, detail=f"Asset={asset_id} not found")
    return result


def insert_asset_value(asset_value: "AssetValue") -> dict:
    """
    Insert a new asset's value.

    Args:
        asset_value (AssetValue): The asset's value to insert.

    Returns:
        dict: The inserted asset's value data.

    Raises:
        HTTPException: If an error occurs.
    """

    try:
        result = crud.insert_asset_value(asset_value)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return result


__all__ = [
    "delete_asset",
    "get_asset",
    "get_assets",
    "get_assets_state",
    "get_assets_values",
    "insert_asset",
    "insert_asset_value",
    "update_asset",
]
