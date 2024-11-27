from typing import TYPE_CHECKING

from fastapi import HTTPException

import app.db.crud as crud


if TYPE_CHECKING:
    from app.models import Structure, StructureCategory


def get_structure(structure_id: int) -> dict:
    """
    Retrieve a structure by its ID.

    Args:
        structure_id (int): The ID of the structure to retrieve.

    Returns:
        dict: The structure data.

    Raises:
        HTTPException: If the structure is not found or an error occurs.
    """

    try:
        result = crud.get_structures(structure_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not result:
        raise HTTPException(status_code=404, detail=f"Structure={structure_id} not found")
    return result[0]


def get_structures() -> list[dict]:
    """
    Retrieve all structures.

    Returns:
        list[dict]: A list of all structures.

    Raises:
        HTTPException: If an error occurs.
    """

    try:
        result = crud.get_structures()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return result


def get_structure_categories(structure_id: int) -> list[dict]:
    """
    Retrieve structure-category links for a specific structure.

    Args:
        structure_id (int): The ID of the structure.

    Returns:
        list[dict]: A list of structure-category links for the structure.

    Raises:
        HTTPException: If the structure is not found or an error occurs.
    """

    try:
        result = crud.get_structures_categories(structure_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not result:
        raise HTTPException(status_code=404, detail=f"Structure={structure_id} not found")
    return result


def get_structure_category(structure_id: int, category_id: int) -> dict:
    """
    Retrieve a specific structure-category link data.

    Args:
        structure_id (int): The ID of the structure.
        category_id (int): The ID of the category.

    Returns:
        dict: The structure-category link data.

    Raises:
        HTTPException: If the structure-category link is not found or an error occurs.
    """

    try:
        result = crud.get_structures_categories(structure_id, category_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not result:
        raise HTTPException(status_code=404, detail=f"Category={category_id} in structure={structure_id} not found")
    return result[0]


def get_structures_categories() -> list[dict]:
    """
    Retrieve all structure-category links.

    Returns:
        list[dict]: A list of all structure-category links.

    Raises:
        HTTPException: If an error occurs.
    """

    try:
        result = crud.get_structures_categories()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return result


def insert_structure(structure: "Structure") -> dict:
    """
    Insert a new structure.

    Args:
        structure (Structure): The structure to insert.

    Returns:
        dict: The inserted structure data.

    Raises:
        HTTPException: If an error occurs.
    """

    try:
        result = crud.insert_structure(structure)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return result


def update_structure(structure: "Structure") -> dict:
    """
    Update an existing structure.

    Args:
        structure (Structure): The structure to update.

    Returns:
        dict: The updated structure data.

    Raises:
        HTTPException: If the structure is not found or an error occurs.
    """

    try:
        result = crud.update_structure(structure)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not result:
        raise HTTPException(status_code=404, detail=f"Structure={structure.structure_id} not found")
    return result


def delete_structure(structure_id: int) -> bool:
    """
    Delete a structure by its ID.

    Args:
        structure_id (int): The ID of the structure to delete.

    Returns:
        bool: True if the structure was deleted, False otherwise.

    Raises:
        HTTPException: If the structure is not found or an error occurs.
    """

    try:
        result = crud.delete_structure(structure_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not result:
        raise HTTPException(status_code=404, detail=f"Structure={structure_id} not found")
    return result


def set_structure_as_current(structure_id: int) -> dict:
    """
    Set a structure as the current structure.

    Args:
        structure_id (int): The ID of the structure to set as current.

    Returns:
        dict: The updated structure data.

    Raises:
        HTTPException: If the structure is not found or an error occurs.
    """

    try:
        result = crud.set_structure_as_current(structure_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not result:
        raise HTTPException(status_code=404, detail=f"Structure={structure_id} not found")
    return result


def insert_structure_category(structure_category: "StructureCategory") -> dict:
    """
    Insert a new structure-category link.

    Args:
        structure_category (StructureCategory): The structure-category link to insert.

    Returns:
        dict: The inserted structure-category link data.

    Raises:
        HTTPException: If an error occurs.
    """

    try:
        result = crud.insert_structure_category(structure_category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return result


def update_structure_category(structure_category: "StructureCategory") -> dict:
    """
    Update an existing structure-category link.

    Args:
        structure_category (StructureCategory): The structure-category link to update.

    Returns:
        dict: The updated structure-category link data.

    Raises:
        HTTPException: If the structure-category link is not found or an error occurs.
    """
    try:
        result = crud.update_structure_category(structure_category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not result:
        raise HTTPException(
            status_code=404,
            detail=(f"Structure/category link with structure_id={structure_category.structure_id} "
                    "and category_id={structure_category.category_id} not found"),
        )
    return result


def delete_structure_category(structure_id: int, category_id: int) -> bool:
    """
    Delete a structure-category link by its structure ID and category ID.

    Args:
        structure_id (int): The ID of the structure.
        category_id (int): The ID of the category.

    Returns:
        bool: True if the structure-category link was deleted, False otherwise.

    Raises:
        HTTPException: If the structure-category link is not found or an error occurs.
    """
    try:
        result = crud.delete_structure_category(structure_id, category_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Structure/category link with structure_id={structure_id} and category_id={category_id} not found",
        )
    return result


__all__ = [
    "delete_structure",
    "delete_structure_category",
    "get_structure",
    "get_structure_categories",
    "get_structure_category",
    "get_structures",
    "get_structures_categories",
    "insert_structure",
    "insert_structure_category",
    "set_structure_as_current",
    "update_structure",
    "update_structure_category",
]
