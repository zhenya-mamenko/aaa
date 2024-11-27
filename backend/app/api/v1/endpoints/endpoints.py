from fastapi import APIRouter

import app.services as services

from app.models import (
    PortfolioResponse,
    ResponseModel,
)


router = APIRouter()
router_path = ""


@router.get("/health")
async def health_check():
    return services.health_check()


@router.get("/portfolio", response_model=ResponseModel[PortfolioResponse])
async def get_portfolio():
    portfolio = services.get_portfolio()
    return ResponseModel(data=[PortfolioResponse(**p) for p in portfolio])
