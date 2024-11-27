from typing import TYPE_CHECKING

from fastapi import HTTPException

import app.db.crud as crud


if TYPE_CHECKING:
    from app.models import ConfigEntry


def get_config() -> list[dict]:
    """
    Retrieve the entire configuration.

    Returns:
        list[dict]: A list of configuration entries.
    """

    try:
        result = crud.get_config()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return result


def get_config_value(config_name: str) -> dict:
    """
    Retrieve a specific configuration value by name.

    Args:
        config_name (str): The name of the configuration entry.

    Returns:
        dict: The configuration entry if found.

    Raises:
        HTTPException: If the configuration entry is not found or an error occurs.
    """

    try:
        result = crud.get_config(config_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not result:
        raise HTTPException(status_code=404, detail=f"Config name='{config_name}' not found")
    return result[0]


def insert_config(config: "ConfigEntry") -> dict:
    """
    Insert a new configuration entry.

    Args:
        config (ConfigEntry): The configuration entry to insert.

    Returns:
        dict: The inserted configuration entry.

    Raises:
        HTTPException: If an error occurs during insertion.
    """

    try:
        result = crud.insert_config(config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return result


def update_config(config: "ConfigEntry") -> dict:
    """
    Update an existing configuration entry.

    Args:
        config (ConfigEntry): The configuration entry to update.

    Returns:
        dict: The updated configuration entry.

    Raises:
        HTTPException: If the configuration entry is not found or an error occurs.
    """

    try:
        result = crud.update_config(config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not result:
        raise HTTPException(status_code=404, detail=f"Class={config.config_name} not found")
    return result


def delete_config(config_name: str) -> bool:
    """
    Delete a configuration entry by name.

    Args:
        config_name (str): The name of the configuration entry to delete.

    Returns:
        bool: True if the deletion was successful, False otherwise.

    Raises:
        HTTPException: If the configuration entry is not found or an error occurs.
    """

    try:
        result = crud.delete_config(config_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not result:
        raise HTTPException(status_code=404, detail=f"Class={config_name} not found")
    return result


__all__ = [
    "delete_config",
    "get_config",
    "get_config_value",
    "insert_config",
    "update_config",
]
