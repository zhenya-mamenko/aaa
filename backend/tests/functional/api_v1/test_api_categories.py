import pytest


@pytest.fixture
def api(api_prefix):
    return f"{api_prefix}/categories"


@pytest.fixture
def name1():
    return "Test 1"


@pytest.mark.asyncio
async def test_get_categories(async_client, api, responses):
    response = await async_client.get(f"{api}")
    assert response.status_code == 200
    result = response.json()
    assert "data" in result
    assert result["data"] == responses["get_categories"]


@pytest.mark.asyncio
async def test_get_category(async_client, api, responses):
    category_id = 1
    response = await async_client.get(f"{api}/{category_id}")
    assert response.status_code == 200
    result = response.json()
    category = list(filter(lambda x: x["category_id"] == category_id, responses["get_categories"]))[0]
    assert result == category

    category_id = 100
    response = await async_client.get(f"{api}/{category_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_insert_category(async_client, api, payloads, name1):
    payload = payloads["category"]
    del payload["category_id"]
    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["category_name"] == payload["category_name"]

    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 500

    payload["category_name"] = ""
    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 422

    payload["category_name"] = name1
    payload["foo"] = "bar"
    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_category(async_client, api, payloads, name1):
    payload = payloads["category"]
    category_id = payload["category_id"]
    del payload["category_id"]
    response = await async_client.put(f"{api}/{category_id}", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["category_name"] == payload["category_name"]

    category_id = 10
    response = await async_client.put(f"{api}/{category_id}", json=payload)
    assert response.status_code == 404

    payload["category_id"] = category_id

    payload["category_name"] = ""
    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 422

    payload["category_name"] = name1
    payload["foo"] = "bar"
    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_category(async_client, api, payloads):
    category_id = 1
    response = await async_client.delete(f"{api}/{category_id}")
    assert response.status_code == 500

    category_id = 100
    response = await async_client.delete(f"{api}/{category_id}")
    assert response.status_code == 404

    payload = payloads["category"]
    del payload["category_id"]
    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 201
    result = response.json()
    category_id = result["category_id"]
    response = await async_client.delete(f"{api}/{category_id}")
    assert response.status_code == 204
