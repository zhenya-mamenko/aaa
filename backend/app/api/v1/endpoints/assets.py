from fastapi import APIRouter

import app.services as services

from app.models import (
    Asset,
    AssetResponse,
    AssetsStateResponse,
    AssetValue,
    AssetsValuesResponse,
    ResponseModel,
)


router = APIRouter()


@router.get("", response_model=ResponseModel[AssetResponse])
async def get_assets():
    assets = services.get_assets()
    return ResponseModel(data=[AssetResponse(**a) for a in assets])


@router.get("/state", response_model=ResponseModel[AssetsStateResponse])
async def get_assets_state():
    state = services.get_assets_state()
    return ResponseModel(data=[AssetsStateResponse(**s) for s in state])


@router.get("/values", response_model=ResponseModel[AssetsValuesResponse])
async def get_assets_values():
    values = services.get_assets_values()
    return ResponseModel(data=[AssetsValuesResponse(**s) for s in values])


@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(asset_id: int):
    asset = services.get_asset(asset_id)
    return AssetResponse(**asset)


@router.post("", response_model=AssetResponse, status_code=201)
async def create_asset(asset: Asset):
    asset = services.insert_asset(asset)
    return AssetResponse(**asset)


@router.post("/values", response_model=AssetsValuesResponse, status_code=201)
async def create_asset_value(asset_value: AssetValue):
    asset_value = services.insert_asset_value(asset_value)
    return AssetsValuesResponse(**asset_value)


@router.put("/{asset_id}", response_model=AssetResponse)
async def update_asset(asset_id: int, asset: Asset):
    asset.asset_id = asset_id
    asset = services.update_asset(asset)
    return AssetResponse(**asset)


@router.delete("/{asset_id}", status_code=204)
async def delete_asset(asset_id: int):
    services.delete_asset(asset_id)
