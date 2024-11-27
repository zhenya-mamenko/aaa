import pytest


@pytest.fixture
def api(api_prefix):
    return f"{api_prefix}/classes"


@pytest.fixture
def name1():
    return "Test 1"


@pytest.mark.asyncio
async def test_get_class(async_client, api, responses):
    class_id = 1
    response = await async_client.get(f"{api}/{class_id}")
    assert response.status_code == 200
    result = response.json()
    _class = list(filter(lambda x: x["class_id"] == class_id, responses["get_classes"]))[0]
    assert result == _class

    class_id = 100
    response = await async_client.get(f"{api}/{class_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_classes(async_client, api, responses):
    response = await async_client.get(f"{api}")
    assert response.status_code == 200
    result = response.json()
    assert "data" in result
    assert result["data"] == responses["get_classes"]


@pytest.mark.asyncio
async def test_insert_class(async_client, api, payloads, name1):
    payload = payloads["class"]
    del payload["class_id"]

    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["class_name"] == payload["class_name"]

    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 500

    payload["class_name"] = ""
    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 422

    payload["class_name"] = name1
    payload["foo"] = "bar"
    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_class(async_client, api, payloads, name1):
    payload = payloads["class"]
    class_id = payload["class_id"]
    del payload["class_id"]
    response = await async_client.put(f"{api}/{class_id}", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["class_name"] == payload["class_name"]

    class_id = 10
    response = await async_client.put(f"{api}/{class_id}", json=payload)
    assert response.status_code == 404

    payload["class_id"] = class_id

    payload["class_name"] = ""
    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 422

    payload["class_name"] = name1
    payload["foo"] = "bar"
    response = await async_client.put(f"{api}/{class_id}", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_class(async_client, api, payloads):
    class_id = 1
    response = await async_client.delete(f"{api}/{class_id}")
    assert response.status_code == 500

    class_id = 100
    response = await async_client.delete(f"{api}/{class_id}")
    assert response.status_code == 404

    payload = payloads["class"]
    del payload["class_id"]
    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 201
    result = response.json()
    class_id = result["class_id"]
    response = await async_client.delete(f"{api}/{class_id}")
    assert response.status_code == 204
