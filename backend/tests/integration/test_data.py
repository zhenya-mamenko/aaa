import json

from app.db.sqlite import read_query


def test_assets():
    query = """
        SELECT
            asset_id,
            category_id,
            asset_name,
            asset_ticker
        FROM assets
    """
    result = read_query(query)
    assert len(result) == 9
    bonds = next(filter(lambda x: x["asset_id"] == 3, result))
    assert bonds
    assert bonds["asset_name"] == "iShares Euro Government Bond 1-3yr UCITS ETF"
    assert bonds["asset_ticker"] == "IBCI"
    assert bonds["category_id"] == 3
    assert len(list(filter(lambda x: x["category_id"] == 6, result))) == 2
    assert len(list(filter(lambda x: x["category_id"] == 7, result))) == 2


def test_assets_values():
    query = """
        SELECT
            value_datetime,
            asset_id,
            amount
        FROM assets_values
    """
    result = read_query(query)
    assert len(result) == 17
    assets = list(filter(lambda x: x["value_datetime"] == "2024-11-15 00:00:00", result))
    assert assets
    assert len(assets) == 5
    assets = list(filter(lambda x: x["value_datetime"] == "2024-11-16 00:00:00", result))
    assert assets
    assert len(assets) == 6
    assets = list(filter(lambda x: x["value_datetime"] == "2024-11-17 00:00:00", result))
    assert assets
    assert len(assets) == 6


def test_categories():
    query = """
        SELECT
            category_id,
            class_id,
            category_name
        FROM categories
    """
    result = read_query(query)
    assert len(result) == 7
    bonds = next(filter(lambda x: x["category_id"] == 4, result))
    assert bonds
    assert bonds["category_name"] == "Corporate bonds"
    assert bonds["class_id"] == 2


def test_classes():
    query = """
        SELECT
            class_id,
            class_name
        FROM classes
    """
    result = read_query(query)
    assert len(result) == 4
    bonds = next(filter(lambda x: x["class_id"] == 2, result))
    assert bonds
    assert bonds["class_name"] == "Bonds"


def test_config():
    query = """
        SELECT
            config_name,
            config_value
        FROM config
    """
    result = read_query(query)
    assert len(result) == 1
    config = next(filter(lambda x: x["config_name"] == "currency", result))
    assert config
    assert json.loads(config["config_value"]) == {"symbol": "€", "position": "after"}


def test_structures():
    query = """
        SELECT
            structure_id,
            structure_name,
            is_current
        FROM structures
    """
    result = read_query(query)
    assert len(result) == 2
    structure = next(filter(lambda x: x["structure_id"] == 1, result))
    assert structure
    assert structure["structure_name"] == "first"
    assert structure["is_current"] == 1
    structure = next(filter(lambda x: x["structure_id"] == 2, result))
    assert structure
    assert structure["structure_name"] == "second"
    assert structure["is_current"] == 0


def test_structure_categories():
    query = """
        SELECT
            structure_id,
            category_id,
            percentile
        FROM structure_categories
    """
    result = read_query(query)
    assert len(result) == 10
    structure = list(filter(lambda x: x["structure_id"] == 1, result))
    assert structure
    assert len(structure) == 4
    assert sum(map(lambda x: x["percentile"], structure)) == 1000
    structure = list(filter(lambda x: x["structure_id"] == 2, result))
    assert structure
    assert len(structure) == 6
    assert sum(map(lambda x: x["percentile"], structure)) == 1000
