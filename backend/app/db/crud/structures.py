from typing import TYPE_CHECKING

from app.db.crud.utils import (
    delete_data_by_id,
    insert_data_from_model,
    update_data_from_model,
)
from app.db.sqlite import (
    get_database_conn as _get_database_conn,
    execute_query as _execute_query,
    read_query as _read_query,
)


if TYPE_CHECKING:
    from app.models import Structure, StructureCategory


def get_structures(structure_id: int | None = None) -> list[dict]:
    """
    Retrieve structures from the database.

    Args:
        structure_id (int | None): The ID of the structure to retrieve. If None, retrieves all structures.

    Returns:
        list[dict]: A list of dictionaries representing the structures.
    """

    query = f"""
        SELECT
            structure_id,
            structure_name,
            structure_date,
            is_current
        FROM structures
        {"WHERE structure_id = ?" if structure_id else ""}
        ORDER BY
            is_current DESC,
            structure_date DESC,
            structure_name
    """

    return _read_query(query, parameters=(structure_id,) if structure_id else ())


def get_structures_categories(structure_id: int | None = None, category_id: int | None = None) -> list[dict]:
    """
    Retrieve structure-category link(s) from the database.

    Args:
        structure_id (int | None): The ID of the structure to retrieve categories for.
        category_id (int | None): The ID of the category to retrieve. Must be used with structure_id.

    Returns:
        list[dict]: A list of dictionaries representing the structure-category link(s).

    Raises:
        ValueError: If category_id is provided without structure_id.
    """

    query = f"""
        SELECT
            structure_id,
            category_id,
            class_name,
            category_name,
            percentile,
            out_percentile
        FROM vw_structure_categories
        {"WHERE structure_id = ?" if structure_id else ""}
        {"  AND category_id = ?" if category_id else ""}
        ORDER BY
            structure_id,
            class_name,
            category_name
    """
    parameters = ()
    if structure_id:
        parameters = (structure_id, category_id) if category_id else (structure_id,)

    return _read_query(query, parameters=parameters)


def insert_structure(structure: "Structure") -> dict:
    """
    Insert a new structure into the database.

    Args:
        structure (Structure): The structure model to insert.

    Returns:
        dict: A dictionary representing the inserted structure.
    """

    id = insert_data_from_model(table_name="structures", id_field="structure_id", model=structure)
    return get_structures(id)[0]


def update_structure(structure: "Structure") -> dict | None:
    """
    Update an existing structure in the database.

    Args:
        structure (Structure): The structure model to update.

    Returns:
        dict | None: A dictionary representing the updated structure, or None if the update failed.
    """

    result = update_data_from_model(table_name="structures", id_field="structure_id", model=structure)
    return get_structures(structure.structure_id)[0] if result else None


def delete_structure(structure_id: int) -> bool:
    """
    Delete a structure from the database.

    Args:
        structure_id (int): The ID of the structure to delete.

    Returns:
        bool: True if the deletion was successful, False otherwise.
    """

    return delete_data_by_id(table_name="structures", id_field="structure_id", id_value=structure_id)


def set_structure_as_current(structure_id: int) -> dict | None:
    """
    Set a structure as the current structure.

    Args:
        structure_id (int): The ID of the structure to set as current.

    Returns:
        dict | None: A dictionary representing the updated structure, or None if the update failed.
    """

    with _get_database_conn() as conn:
        query = """
            UPDATE structures
            SET is_current = 0
            WHERE is_current = 1
        """
        _execute_query(query, conn=conn)

        query = """
            UPDATE structures
            SET is_current = 1
            WHERE structure_id = ?
        """
        result = _execute_query(query, parameters=(structure_id,), conn=conn) == 1
        if not result:
            conn.rollback()

    return get_structures(structure_id)[0] if result else None


def insert_structure_category(structure_category: "StructureCategory") -> dict:
    """
    Insert a new structure-category link into the database.

    Args:
        structure_category (StructureCategory): The model to insert.

    Returns:
        dict: A dictionary representing the inserted data.
    """

    insert_data_from_model(
        table_name="structure_categories",
        id_field=("structure_id", "category_id"),
        model=structure_category,
        auto_increment_id=False,
    )
    return get_structures_categories(
        structure_id=structure_category.structure_id, category_id=structure_category.category_id
    )[0]


def update_structure_category(structure_category: "StructureCategory") -> dict | None:
    """
    Update an existing structure-category link in the database.

    Args:
        structure_category (StructureCategory): The model to update.

    Returns:
        dict | None: A dictionary representing the updated data, or None if the update failed.
    """

    result = update_data_from_model(
        table_name="structure_categories", id_field=("structure_id", "category_id"), model=structure_category
    )
    return (
        get_structures_categories(
            structure_id=structure_category.structure_id, category_id=structure_category.category_id
        )[0]
        if result
        else None
    )


def delete_structure_category(structure_id: int, category_id: int) -> bool:
    """
    Delete a structure-category link from the database.

    Args:
        structure_id (int): The ID of the structure.
        category_id (int): The ID of the category.

    Returns:
        bool: True if the deletion was successful, False otherwise.
    """

    return delete_data_by_id(
        table_name="structure_categories",
        id_field=("structure_id", "category_id"),
        id_value=(structure_id, category_id),
    )


__all__ = [
    "delete_structure",
    "delete_structure_category",
    "get_structures",
    "get_structures_categories",
    "insert_structure",
    "insert_structure_category",
    "set_structure_as_current",
    "update_structure",
    "update_structure_category",
]
