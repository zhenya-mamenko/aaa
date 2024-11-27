import pytest

from app.models import ConfigEntry


@pytest.fixture
def api(api_prefix):
    return f"{api_prefix}/config"


@pytest.fixture
def name1():
    return "Test 1"


@pytest.fixture
def config_value():
    return dict(symbol="$", position="before")


@pytest.fixture
def config_name():
    return "currency"


@pytest.fixture
def config_entry(name1, config_value):
    return ConfigEntry(config_name=name1, config_value=config_value)


@pytest.mark.asyncio
async def test_get_config(async_client, api, responses):
    response = await async_client.get(f"{api}")
    assert response.status_code == 200
    result = response.json()
    assert "data" in result
    assert result["data"] == responses["get_config"]


@pytest.mark.asyncio
async def test_get_config_value(async_client, api, config_name, name1, responses):
    response = await async_client.get(f"{api}/{config_name}")
    assert response.status_code == 200
    result = response.json()
    config = list(filter(lambda x: x["config_name"] == config_name, responses["get_config"]))[0]
    assert result == ConfigEntry(**config).model_dump()

    response = await async_client.get(f"{api}/{name1}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_insert_config(async_client, api, config_entry, name1):
    payload = config_entry.model_dump()

    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["config_name"] == payload["config_name"]

    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 500

    payload["config_name"] = ""
    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 422

    payload["config_name"] = name1
    payload["foo"] = "bar"
    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_config(async_client, api, payloads, name1):
    payload = payloads["config"]
    config_name = payload["config_name"]
    del payload["config_name"]
    response = await async_client.put(f"{api}/{config_name}", json=payload)
    assert response.status_code == 200

    config_name = name1
    response = await async_client.put(f"{api}/{config_name}", json=payload)
    assert response.status_code == 404

    payload["config_name"] = ""
    response = await async_client.post(f"{api}", json=payload)
    assert response.status_code == 422

    config_name = name1
    payload["foo"] = "bar"
    response = await async_client.put(f"{api}/{config_name}", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_config(async_client, api, config_name, name1):
    response = await async_client.delete(f"{api}/{name1}")
    assert response.status_code == 404

    response = await async_client.delete(f"{api}/{config_name}")
    assert response.status_code == 204
