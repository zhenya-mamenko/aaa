from fastapi import APIRouter

import app.services as services

from app.models import (
    ResponseModel,
    Structure,
    StructureCategory,
    StructureCategoryResponse,
)


router = APIRouter()


@router.get("", response_model=ResponseModel[Structure])
async def get_structures():
    structures = services.get_structures()
    return ResponseModel(data=[Structure(**a) for a in structures])


@router.get("/categories", response_model=ResponseModel[StructureCategoryResponse])
async def get_structures_categories():
    categories = services.get_structures_categories()
    return ResponseModel(data=[StructureCategoryResponse(**a) for a in categories])


@router.get("/{structure_id}/categories", response_model=ResponseModel[StructureCategoryResponse])
async def get_structure_categories(structure_id: int):
    categories = services.get_structure_categories(structure_id)
    return ResponseModel(data=[StructureCategoryResponse(**a) for a in categories])


@router.get("/{structure_id}/categories/{category_id}", response_model=StructureCategoryResponse)
async def get_structure_category(structure_id: int, category_id: int):
    category = services.get_structure_category(structure_id, category_id)
    return StructureCategoryResponse(**category)


@router.get("/{structure_id}", response_model=Structure)
async def get_structure(structure_id: int):
    structure = services.get_structure(structure_id)
    return Structure(**structure)


@router.post("/{structure_id}/categories", response_model=StructureCategoryResponse, status_code=201)
async def create_structure_category(structure_id: int, structure_category: StructureCategory):
    structure_category.structure_id = structure_id
    structure_category = services.insert_structure_category(structure_category)
    return StructureCategoryResponse(**structure_category)


@router.post("", response_model=Structure, status_code=201)
async def create_structure(structure: Structure):
    structure = services.insert_structure(structure)
    return Structure(**structure)


@router.put("/{structure_id}/categories/{category_id}", response_model=StructureCategoryResponse)
async def update_structure_category(structure_id: int, category_id: int, structure_category: StructureCategory):
    structure_category.structure_id = structure_id
    structure_category.category_id = category_id
    structure_category = services.update_structure_category(structure_category)
    return StructureCategoryResponse(**structure_category)


@router.put("/{structure_id}", response_model=Structure)
async def update_structure(structure_id: int, structure: Structure):
    structure.structure_id = structure_id
    structure = services.update_structure(structure)
    return Structure(**structure)


@router.delete("/{structure_id}/categories/{category_id}", status_code=204)
async def delete_structure_category(structure_id: int, category_id: int):
    services.delete_structure_category(structure_id, category_id)


@router.delete("/{structure_id}", status_code=204)
async def delete_structure(structure_id: int):
    services.delete_structure(structure_id)


@router.patch("/{structure_id}", response_model=Structure)
async def set_structure_as_current(structure_id: int):
    structure = services.set_structure_as_current(structure_id)
    return Structure(**structure)
