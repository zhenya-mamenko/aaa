import pytest


@pytest.mark.asyncio
async def test_read_root(async_client):
    response = await async_client.get("")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


@pytest.mark.asyncio
async def test_health_check(async_client, api_prefix):
    response = await async_client.get(f"{api_prefix}/health")
    assert response.status_code == 200
    assert response.json() == "OK"


@pytest.mark.asyncio
async def test_portfolio(async_client, api_prefix, responses):
    response = await async_client.get(f"{api_prefix}/portfolio")
    assert response.status_code == 200
    result = response.json()
    assert "data" in result
    assert result["data"] == responses["get_portfolio"]
