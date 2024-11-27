import pytest

from pydantic import BaseModel

from app.db.creator import (
    parse_args,
    run,
)
from app.db.crud.utils import (
    create_parameters_from_model,
    extract_create_stmts_objects,
)


def test_create_parameters_from_model():
    class Model(BaseModel):
        field1: str
        field2: str
        field3: str | None = None
        field4: str

    model = Model(field1="value1", field2="value2", field4="value4")
    template, fields, parameters = create_parameters_from_model(model)
    assert template == "?, ?, ?"
    assert fields == ["field1", "field2", "field4"]
    assert parameters == ("value1", "value2", "value4")

    template, fields, parameters = create_parameters_from_model(model, exclude_fields=("field2",))
    assert template == "?, ?"
    assert fields == ["field1", "field4"]
    assert parameters == ("value1", "value4")

    template, fields, parameters = create_parameters_from_model(model, only_fields=("field1", "field2"))
    assert template == "?, ?"
    assert fields == ["field1", "field2"]
    assert parameters == ("value1", "value2")

    with pytest.raises(ValueError) as exc_info:
        create_parameters_from_model(model, only_fields=("field1", "field2", "field5"))
    assert "Fields={'field5'} are not in the model." in str(exc_info.value)

    template, fields, parameters, max_query = create_parameters_from_model(model, get_max_data=("table", "id"))
    assert template == "?, ?, ?, (SELECT COALESCE(MAX(id), 0) + 1 FROM table)"
    assert fields == ["field1", "field2", "field4", "id"]
    assert parameters == ("value1", "value2", "value4")
    assert max_query == "SELECT MAX(id) as id FROM table;"

    with pytest.raises(ValueError) as exc_info:
        create_parameters_from_model(model, get_max_data=("table", "field1"))
    assert "Field field1 must be excluded from the model." in str(exc_info.value)


def test_extract_create_stmts_objects(schema_files):
    result = extract_create_stmts_objects(schema_files[0], "TABLE")
    assert len(result) == 7

    result = extract_create_stmts_objects(schema_files[1], "VIEW")
    assert len(result) == 6

    with pytest.raises(FileNotFoundError) as exc_info:
        extract_create_stmts_objects("tmp/qq.tmp", "TABLE")
    assert "File not found: tmp/qq.tmp" in str(exc_info.value)


def test_parse_args():
    sys_args = ["test.db", "-s", "schema.sql", "-f", "data.csv", "-d", "|"]
    result = parse_args(sys_args)
    assert result == {
        "db_name": "test.db",
        "schema": ["schema.sql"],
        "data": ["data.csv"],
        "delimeter": ord("|"),
    }

    sys_args = ["test.db"]
    result = parse_args(sys_args)
    assert result == {
        "db_name": "test.db",
        "schema": None,
        "data": None,
        "delimeter": ord("|"),
    }


def test_run_db_params_dont_exist():
    with pytest.raises(ValueError) as exc_info:
        run()
    assert "Either db_name or db_conn must be provided" in str(exc_info.value)
