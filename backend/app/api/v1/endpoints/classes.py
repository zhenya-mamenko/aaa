from fastapi import APIRouter

import app.services as services

from app.models import (
    AssetClass,
    ResponseModel,
)


router = APIRouter()


@router.get("", response_model=ResponseModel[AssetClass])
async def get_asset_classes():
    classes = services.get_asset_classes()
    return ResponseModel(data=[AssetClass(**c) for c in classes])


@router.get("/{class_id}", response_model=AssetClass)
async def get_asset_class(class_id: int):
    _class = services.get_asset_class(class_id)
    return AssetClass(**_class)


@router.post("", response_model=AssetClass, status_code=201)
async def create_asset_class(asset_class: AssetClass):
    asset_class = services.insert_asset_class(asset_class)
    return AssetClass(**asset_class)


@router.put("/{class_id}", response_model=AssetClass)
async def update_asset_class(class_id: int, asset_class: AssetClass):
    asset_class.class_id = class_id
    asset_class = services.update_asset_class(asset_class)
    return AssetClass(**asset_class)


@router.delete("/{class_id}", status_code=204)
async def delete_asset_class(class_id: int):
    services.delete_asset_class(class_id)
