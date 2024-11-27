# ruff: noqa: F403 F405
import pytest

from fastapi import HTTPException

from app.db.sqlite import get_database_conn
from app.models import Structure, StructureCategory

from app.services.structures import *


@pytest.fixture
def name1():
    return "Test 1"


@pytest.fixture
def name2():
    return "Test 2"


@pytest.fixture
def data_name():
    return "first"


@pytest.fixture
def data_id():
    return 1


@pytest.fixture
def structure(name1):
    return Structure(structure_id=1, structure_name=name1, is_current=False)


@pytest.fixture
def structure_no_id(name1):
    return Structure(structure_name=name1, is_current=False)


@pytest.fixture
def data_category_id():
    return 4


@pytest.fixture
def data_category_name():
    return "Corporate bonds"


@pytest.fixture
def data_category_class_name():
    return "Bonds"


@pytest.fixture
def structure_category(data_id, data_category_id):
    return StructureCategory(structure_id=data_id, category_id=data_category_id, percentile=80)


def test_get_structure(data_name, data_id):
    structure = get_structure(data_id)
    assert structure
    assert structure["structure_name"] == data_name

    with pytest.raises(HTTPException) as exc_info:
        get_structure(100)
    assert exc_info.value.status_code == 404

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        get_structure(data_id)
    assert exc_info.value.status_code == 500


def test_get_structures(data_name, data_id):
    result = get_structures()
    assert result
    assert len(result) == 2
    structure = next(filter(lambda x: x["structure_id"] == data_id, result))
    assert structure["structure_name"] == data_name

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        get_structures()
    assert exc_info.value.status_code == 500


def test_get_structures_categories(data_id, data_category_id, data_category_name, data_category_class_name):
    result = get_structures_categories()
    assert result
    assert len(result) == 10
    structure = list(filter(lambda x: x["structure_id"] == data_id, result))
    assert len(structure) == 4
    assert structure[0]["class_name"] == data_category_class_name
    assert structure[0]["category_name"] == data_category_name
    assert sum([x["percentile"] for x in structure]) == 1000

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        get_structures_categories()
    assert exc_info.value.status_code == 500


def test_get_structure_categories(data_id, data_category_id, data_category_name, data_category_class_name):
    structure = get_structure_categories(data_id)
    assert structure
    assert len(structure) == 4
    category = next(filter(lambda x: x["category_id"] == data_category_id, structure))
    assert category
    assert category["class_name"] == data_category_class_name
    assert category["category_name"] == data_category_name
    assert sum([x["percentile"] for x in structure]) == 1000

    with pytest.raises(HTTPException) as exc_info:
        get_structure_categories(100)
    assert exc_info.value.status_code == 404

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        get_structure_categories(data_id)
    assert exc_info.value.status_code == 500


def test_get_structure_category(data_id, data_category_id, data_category_name, data_category_class_name):
    category = get_structure_category(data_id, data_category_id)
    assert category
    assert category["class_name"] == data_category_class_name
    assert category["category_name"] == data_category_name

    with pytest.raises(HTTPException) as exc_info:
        get_structure_category(100, 1)
    assert exc_info.value.status_code == 404

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        get_structure_category(data_id, data_category_id)
    assert exc_info.value.status_code == 500


def test_insert_structure(name1, name2, structure_no_id):
    result = insert_structure(structure_no_id)
    assert result
    assert result["structure_name"] == name1

    with pytest.raises(HTTPException) as exc_info:
        insert_structure(structure_no_id)
    assert exc_info.value.status_code == 500

    get_database_conn().close()
    structure.structure_name = name2
    with pytest.raises(HTTPException) as exc_info:
        insert_structure(structure_no_id)
    assert exc_info.value.status_code == 500


def test_update_structure(name1, structure):
    _structure = structure

    result = update_structure(structure)
    assert result
    assert result["structure_name"] == name1

    _structure.structure_id = 100
    with pytest.raises(HTTPException) as exc_info:
        update_structure(_structure)
    assert exc_info.value.status_code == 404

    _structure.structure_id = 2
    with pytest.raises(HTTPException) as exc_info:
        update_structure(_structure)
    assert exc_info.value.status_code == 500

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        update_structure(structure)
    assert exc_info.value.status_code == 500


def test_delete_structure(name1, structure_no_id):
    with pytest.raises(HTTPException) as exc_info:
        delete_structure(1)
    assert exc_info.value.status_code == 500

    with pytest.raises(HTTPException) as exc_info:
        delete_structure(100)
    assert exc_info.value.status_code == 404

    result = insert_structure(structure_no_id)
    assert result
    id = result["structure_id"]

    assert delete_structure(id)

    with pytest.raises(HTTPException) as exc_info:
        delete_structure(id)
    assert exc_info.value.status_code == 404

    result = insert_structure(structure_no_id)
    assert result
    id = result["structure_id"]

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        delete_structure(id)
    assert exc_info.value.status_code == 500


def test_set_structure_as_current():
    result = set_structure_as_current(2)
    assert result
    assert result["is_current"] == 1

    with pytest.raises(HTTPException) as exc_info:
        set_structure_as_current(100)
    assert exc_info.value.status_code == 404

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        set_structure_as_current(2)
    assert exc_info.value.status_code == 500


def test_insert_structure_category(structure_category):
    delete_structure_category(structure_category.structure_id, structure_category.category_id)

    result = insert_structure_category(structure_category)
    assert result
    assert result["structure_id"] == structure_category.structure_id
    assert result["category_id"] == structure_category.category_id

    with pytest.raises(HTTPException) as exc_info:
        insert_structure_category(structure_category)
    assert exc_info.value.status_code == 500

    structure_category.category_id = 5
    structure_category.percentile = 100
    with pytest.raises(HTTPException) as exc_info:
        insert_structure_category(structure_category)
    assert exc_info.value.status_code == 500

    get_database_conn().close()
    structure_category.category_id = 6
    with pytest.raises(HTTPException) as exc_info:
        insert_structure_category(structure_category)
    assert exc_info.value.status_code == 500


def test_update_structure_category(structure_category):
    structure_category.percentile = 100
    result = update_structure_category(structure_category)
    assert result
    assert result["percentile"] == 100

    structure_category.category_id = 100
    with pytest.raises(HTTPException) as exc_info:
        update_structure_category(structure_category)
    assert exc_info.value.status_code == 404

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        update_structure_category(structure_category)
    assert exc_info.value.status_code == 500


def test_delete_structure_category(data_id, data_category_id, structure_category):
    with pytest.raises(HTTPException) as exc_info:
        delete_structure_category(data_id, 100)
    assert exc_info.value.status_code == 404

    assert delete_structure_category(data_id, data_category_id)

    with pytest.raises(HTTPException) as exc_info:
        delete_structure_category(data_id, data_category_id)
    assert exc_info.value.status_code == 404

    result = insert_structure_category(structure_category)
    assert result

    get_database_conn().close()
    with pytest.raises(HTTPException) as exc_info:
        delete_structure_category(data_id, data_category_id)
    assert exc_info.value.status_code == 500
