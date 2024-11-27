from typing import TYPE_CHECKING

from app.db.crud.utils import (
    delete_data_by_id,
    insert_data_from_model,
    update_data_from_model,
)
from app.db.sqlite import read_query as _read_query


if TYPE_CHECKING:
    from app.models import ConfigEntry


def get_config(config_name: str | None = None) -> list[dict]:
    """
    Retrieve configuration entries from the database.

    Args:
        config_name (str | None): The name of the configuration entry to retrieve. If None, retrieves all entries.

    Returns:
        list: A list of configuration entries.
    """

    query = f"""
        SELECT
            config_name,
            config_value
        FROM config
        {"WHERE config_name = ?" if config_name else ""}
        ORDER BY
            config_name
    """
    return _read_query(query, parameters=(config_name,) if config_name else ())


def insert_config(config: "ConfigEntry") -> dict:
    """
    Insert a new configuration entry into the database.

    Args:
        config (ConfigEntry): The configuration entry to insert.

    Returns:
        dict: The inserted configuration entry.
    """

    insert_data_from_model(table_name="config", id_field="config_name", model=config, auto_increment_id=False)
    return get_config(config.config_name)[0]


def update_config(config: "ConfigEntry") -> dict | None:
    """
    Update an existing configuration entry in the database.

    Args:
        config (ConfigEntry): The configuration entry to update.

    Returns:
        dict | None: The updated configuration entry, or None if the update failed.
    """

    result = update_data_from_model(table_name="config", id_field="config_name", model=config)
    return get_config(config.config_name)[0] if result else None


def delete_config(config_name: str) -> bool:
    """
    Delete a configuration entry from the database.

    Args:
        config_name (str): The name of the configuration entry to delete.

    Returns:
        bool: True if the deletion was successful, False otherwise.
    """

    return delete_data_by_id(table_name="config", id_field="config_name", id_value=config_name)


__all__ = [
    "delete_config",
    "get_config",
    "insert_config",
    "update_config",
]
