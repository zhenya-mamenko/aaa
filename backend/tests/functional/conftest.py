import json
import os

import pytest
import pytest_asyncio

from httpx import (
    AsyncClient,
    ASGITransport,
)

from app import fastapi_app


@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
def responses():
    root_dir = os.path.abspath(os.path.curdir)
    responses_dir = os.path.join(root_dir, "tests", "fixtures", "responses")
    responses_dict = {}
    for filename in os.listdir(responses_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(responses_dir, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                responses_dict[filename.split(".")[0]] = json.load(file)
    return responses_dict


@pytest.fixture
def payloads():
    root_dir = os.path.abspath(os.path.curdir)
    payloads_dir = os.path.join(root_dir, "tests", "fixtures", "payloads")
    payloads_dict = {}
    for filename in os.listdir(payloads_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(payloads_dir, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                payloads_dict[filename.split(".")[0]] = json.load(file)
    return payloads_dict
