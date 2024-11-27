from fastapi import APIRouter

import app.services as services

from app.models import (
    AssetCategory,
    AssetCategoryResponse,
    ResponseModel,
)


router = APIRouter()


@router.get("", response_model=ResponseModel[AssetCategoryResponse])
async def get_asset_categories():
    categories = services.get_asset_categories()
    return ResponseModel(data=[AssetCategoryResponse(**c) for c in categories])


@router.get("/{category_id}", response_model=AssetCategoryResponse)
async def get_asset_category(category_id: int):
    category = services.get_asset_category(category_id)
    return AssetCategoryResponse(**category)


@router.post("", response_model=AssetCategoryResponse, status_code=201)
async def create_asset_category(category: AssetCategory):
    category = services.insert_asset_category(category)
    return AssetCategoryResponse(**category)


@router.put("/{category_id}", response_model=AssetCategoryResponse)
async def update_asset_category(category_id: int, category: AssetCategory):
    category.category_id = category_id
    category = services.update_asset_category(category)
    return AssetCategoryResponse(**category)


@router.delete("/{category_id}", status_code=204)
async def delete_asset_category(category_id: int):
    services.delete_asset_category(category_id)
