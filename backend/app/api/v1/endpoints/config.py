from fastapi import APIRouter

import app.services as services

from app.models import (
    ConfigEntry,
    ResponseModel,
)


router = APIRouter()


@router.get("", response_model=ResponseModel[ConfigEntry])
async def get_config():
    config = services.get_config()
    return ResponseModel(data=[ConfigEntry(**c) for c in config])


@router.get("/{config_name}", response_model=ConfigEntry)
async def get_config_value(config_name: str):
    config_value = services.get_config_value(config_name)
    return ConfigEntry(**config_value)


@router.post("", response_model=ConfigEntry, status_code=201)
async def create_config(config: ConfigEntry):
    config = services.insert_config(config)
    return ConfigEntry(**config)


@router.put("/{config_name}", response_model=ConfigEntry)
async def update_config(config_name: str, config: ConfigEntry):
    config.config_name = config_name
    config = services.update_config(config)
    return ConfigEntry(**config)


@router.delete("/{config_name}", status_code=204)
async def delete_config(config_name: str):
    services.delete_config(config_name)
