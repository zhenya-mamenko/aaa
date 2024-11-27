import pytest


@pytest.fixture
def api(api_prefix):
    return f"{api_prefix}/assets"


@pytest.fixture
def name1():
    return "Test 1"


@pytest.mark.asyncio
async def test_get_asset(async_client, api, responses):
    asset_id = 1
    response = await async_client.get(f"{api}/{asset_id}")
    assert response.status_code == 200
    result = response.json()
    asset = list(filter(lambda x: x["asset_id"] == asset_id, responses["get_assets"]))[0]
    assert result == asset

    asset_id = 100
    response = await async_client.get(f"{api}/{asset_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_assets(async_client, api, responses):
    response = await async_client.get(f"{api}")
    assert response.status_code == 200
    result = response.json()
    assert "data" in result
    assert result["data"] == responses["get_assets"]


@pytest.mark.asyncio
async def test_get_assets_state(async_client, api, responses):
    response = await async_client.get(f"{api}/state")
    assert response.status_code == 200
    result = response.json()
    assert "data" in result
    assert result["data"] == responses["get_assets_state"]


@pytest.mark.asyncio
async def test_get_assets_values(async_client, api, responses):
    response = await async_client.get(f"{api}/values")
    assert response.status_code == 200
    result = response.json()
    assert "data" in result
    assert result["data"] == responses["get_assets_values"]


@pytest.mark.asyncio
async def test_insert_asset(async_client, api, payloads, name1):
    payload = payloads["asset"]
    del payload["asset_id"]

    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["asset_name"] == payload["asset_name"]

    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 500

    payload["asset_name"] = ""
    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 422

    payload["asset_name"] = name1
    payload["foo"] = "bar"
    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_asset(async_client, api, payloads, name1):
    payload = payloads["asset"]
    asset_id = payload["asset_id"]
    del payload["asset_id"]
    response = await async_client.put(f"{api}/{asset_id}", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["asset_name"] == payload["asset_name"]

    asset_id = 10
    response = await async_client.put(f"{api}/{asset_id}", json=payload)
    assert response.status_code == 404

    payload["asset_id"] = asset_id

    payload["asset_name"] = ""
    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 422

    payload["asset_name"] = name1
    payload["foo"] = "bar"
    response = await async_client.put(f"{api}/{asset_id}", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_asset(async_client, api, payloads):
    asset_id = 1
    response = await async_client.delete(f"{api}/{asset_id}")
    assert response.status_code == 500

    asset_id = 100
    response = await async_client.delete(f"{api}/{asset_id}")
    assert response.status_code == 404

    payload = payloads["asset"]
    del payload["asset_id"]
    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 201
    result = response.json()
    asset_id = result["asset_id"]
    response = await async_client.delete(f"{api}/{asset_id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_insert_asset_value(async_client, api, payloads):
    payload = payloads["asset_value"]

    response = await async_client.post(f"{api}/values", json=payload)
    assert response.status_code == 201
    result = response.json()
    print(result)
    assert result["asset_id"] == payload["asset_id"]
    assert result["asset_value_datetime"]

    payload["foo"] = "bar"
    response = await async_client.post(f"{api}/values", json=payload)
    assert response.status_code == 422

    del payload["foo"]
    del payload["asset_id"]
    response = await async_client.post(f"{api}/values", json=payload)
    assert response.status_code == 422

