import pytest

from app.models import Structure


@pytest.fixture
def api(api_prefix):
    return f"{api_prefix}/structures"


@pytest.fixture
def name1():
    return "Test 1"


@pytest.mark.asyncio
async def test_get_structures(async_client, api, responses):
    response = await async_client.get(f"{api}")
    assert response.status_code == 200
    result = response.json()
    assert "data" in result
    assert [Structure(**s) for s in result["data"]] == [Structure(**s) for s in responses["get_structures"]]


@pytest.mark.asyncio
async def test_get_structure(async_client, api, responses):
    structure_id = 1
    response = await async_client.get(f"{api}/{structure_id}")
    assert response.status_code == 200
    result = response.json()
    structure = list(filter(lambda x: x["structure_id"] == structure_id, responses["get_structures"]))[0]
    assert Structure(**result) == Structure(**structure)

    structure_id = 10
    response = await async_client.get(f"{api}/{structure_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_structures_categories(async_client, api, responses):
    response = await async_client.get(f"{api}/categories")
    assert response.status_code == 200
    result = response.json()
    assert "data" in result
    assert result["data"] == responses["get_structures_categories"]


@pytest.mark.asyncio
async def test_get_structure_categories(async_client, api, responses):
    structure_id = 1
    response = await async_client.get(f"{api}/{structure_id}/categories")
    assert response.status_code == 200
    result = response.json()
    assert "data" in result
    structures = list(filter(lambda x: x["structure_id"] == structure_id, responses["get_structures_categories"]))
    assert result["data"] == structures


@pytest.mark.asyncio
async def test_get_structure_category(async_client, api, responses):
    structure_id = 1
    category_id = 1
    response = await async_client.get(f"{api}/{structure_id}/categories/{category_id}")
    assert response.status_code == 200
    result = response.json()
    structure = list(filter(
        lambda x: x["structure_id"] == structure_id and x["category_id"] == category_id, responses["get_structures_categories"]
    ))[0]
    assert result == structure


@pytest.mark.asyncio
async def test_insert_structure(async_client, api, payloads, name1):
    payload = payloads["structure"]
    del payload["structure_id"]

    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["structure_name"] == payload["structure_name"]

    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 500

    payload["structure_name"] = ""
    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 422

    payload["structure_name"] = name1
    payload["foo"] = "bar"
    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_structure(async_client, api, payloads, name1):
    payload = payloads["structure"]
    structure_id = payload["structure_id"]
    del payload["structure_id"]
    response = await async_client.put(f"{api}/{structure_id}", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["structure_name"] == payload["structure_name"]

    structure_id = 10

    payload["structure_id"] = structure_id
    response = await async_client.put(f"{api}/{structure_id}", json=payload)
    assert response.status_code == 404

    payload["structure_name"] = ""
    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 422

    payload["structure_name"] = name1
    payload["foo"] = "bar"
    response = await async_client.put(f"{api}/{structure_id}", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_structure(async_client, api, payloads):
    structure_id = 1
    response = await async_client.delete(f"{api}/{structure_id}")
    assert response.status_code == 500

    structure_id = 100
    response = await async_client.delete(f"{api}/{structure_id}")
    assert response.status_code == 404

    payload = payloads["structure"]
    del payload["structure_id"]
    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 201
    result = response.json()
    structure_id = result["structure_id"]
    response = await async_client.delete(f"{api}/{structure_id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_set_structure_as_default(async_client, api):
    structure_id = 2
    response = await async_client.patch(f"{api}/{structure_id}")
    assert response.status_code == 200

    structure_id = 100
    response = await async_client.delete(f"{api}/{structure_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_insert_structure_category(async_client, api, payloads):
    structure_id, category_id = 1, 4
    response = await async_client.delete(f"{api}/{structure_id}/categories/{category_id}")
    assert response.status_code == 204

    payload = payloads["structure_category"]

    response = await async_client.post(f"{api}/{structure_id}/categories", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["percentile"] == payload["percentile"]

    response = await async_client.post(f"{api}/{structure_id}/categories", json=payload)
    assert response.status_code == 500

    payload["category_id"] = 4
    payload["percentile"] = 100
    response = await async_client.post(f"{api}/{structure_id}/categories", json=payload)
    assert response.status_code == 500


    payload["percentile"] = 5000
    response = await async_client.post(f"{api}/{structure_id}/categories", json=payload)
    assert response.status_code == 422

    payload["percentile"] = 100
    payload["foo"] = "bar"
    response = await async_client.post(f"{api}/{structure_id}/categories", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_structure_category(async_client, api, payloads):
    payload = payloads["structure_category"]
    structure_id = payload["structure_id"]
    category_id = 1
    payload["category_id"] = 1
    response = await async_client.put(f"{api}/{structure_id}/categories/{category_id}", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["percentile"] == payload["percentile"]

    payload["percentile"] = 500
    response = await async_client.post(f"{api}/{structure_id}/categories", json=payload)
    assert response.status_code == 500

    category_id = 10
    response = await async_client.put(f"{api}/{structure_id}/categories/{category_id}", json=payload)
    assert response.status_code == 404

    payload["category_id"] = category_id

    payload["percentile"] = 5000
    response = await async_client.post(f"{api}/{structure_id}/categories", json=payload)
    assert response.status_code == 422

    payload["percentile"] = 100
    payload["foo"] = "bar"
    response = await async_client.put(f"{api}/{structure_id}/categories/{category_id}", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_structure_category(async_client, api, payloads):
    structure_id, category_id = 1, 1
    response = await async_client.delete(f"{api}/{structure_id}/categories/{category_id}")
    assert response.status_code == 204

    category_id = 100
    response = await async_client.delete(f"{api}/{structure_id}/categories/{category_id}")
    assert response.status_code == 404
