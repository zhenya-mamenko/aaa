import json
import re

from pydantic import BaseModel as _BaseModel

from app.db.sqlite import (
    execute_query as _execute_query,
    get_database_conn as _get_database_conn,
    read_query as _read_query,
)


def create_parameters_from_model(
    model: _BaseModel,
    /,
    exclude_fields: tuple[str] | None = None,
    only_fields: tuple[str] | None = None,
    get_max_data: tuple | None = None,
) -> tuple:
    """
    Create SQL parameters from a Pydantic model.

    Args:
        model (_BaseModel): The Pydantic model instance.
        exclude_fields (tuple[str] | None, optional): Fields to exclude from the model. Defaults to None.
        only_fields (tuple[str] | None, optional): Fields to include from the model. Defaults to None.
        get_max_data (tuple | None, optional): Tuple containing table name and field to get max value. Defaults to None.

    Returns:
        tuple: A tuple containing the SQL template, fields, parameters, and optionally a max query.
    """

    exclude_fields = exclude_fields or ()
    model_dump = {
        k: json.dumps(v) if type(v).__name__ in ["list", "dict"] else v for k, v in model.model_dump().items()
    }

    if only_fields:
        fields = [field for field in only_fields if field in model_dump]
        if len(fields) != len(only_fields):
            raise ValueError(f"Fields={set(fields) ^ set(only_fields)} are not in the model.")
    else:
        fields = [field for field, value in model_dump.items() if field not in exclude_fields and value is not None]
    parameters = tuple([model_dump[field] for field in fields])
    template = ", ".join(["?" for _ in parameters])

    if get_max_data:
        table_name, field = get_max_data
        if field in fields:
            raise ValueError(f"Field {field} must be excluded from the model.")
        fields.append(field)
        template += f", (SELECT COALESCE(MAX({field}), 0) + 1 FROM {table_name})"
        max_query = f"SELECT MAX({field}) as {field} FROM {table_name};"
        return template, fields, parameters, max_query

    return template, fields, parameters


def insert_data_from_model(
    *, table_name: str, id_field: tuple | str, model: _BaseModel, auto_increment_id: bool = True
) -> int | str | None:
    """
    Insert data into a table from a Pydantic model.

    Args:
        table_name (str): The name of the table to insert data into.
        id_field (tuple | str): The field(s) representing the ID.
        model (_BaseModel): The Pydantic model instance.
        auto_increment_id (bool, optional): Whether the ID is auto-incremented. Defaults to True.

    Returns:
        int | str | None: The ID of the inserted row if auto_increment_id is True, otherwise None.
    """

    if auto_increment_id:
        if isinstance(id_field, tuple):
            raise ValueError("auto_increment_id must be False if id_field is a tuple.")
        template, fields, parameters, q = create_parameters_from_model(model, get_max_data=(table_name, id_field))
    else:
        template, fields, parameters = create_parameters_from_model(model)

    with _get_database_conn() as conn:
        query = f"""
            INSERT INTO {table_name} (
                {", ".join(fields)}
            ) VALUES (
                {template}
            );
        """
        _execute_query(query, parameters=parameters, conn=conn)
        if auto_increment_id:
            id = _read_query(q, conn=conn)[0][id_field]
            return id

    return None


def update_data_from_model(*, table_name: str, id_field: tuple | str, model: _BaseModel) -> bool:
    """
    Update data in a table from a Pydantic model.

    Args:
        table_name (str): The name of the table to update data in.
        id_field (tuple | str): The field(s) representing the ID.
        model (_BaseModel): The Pydantic model instance.

    Returns:
        bool: True if the update was successful, False otherwise.
    """

    if isinstance(id_field, str):
        id_field = (id_field,)

    _, fields, parameters = create_parameters_from_model(model, exclude_fields=id_field)

    query = f"""
        UPDATE {table_name}
        SET
            {", ".join([f"{field} = ?" for field in fields])}
        WHERE
            {' AND '.join([f'{f} = ?' for f in id_field])};
    """
    parameters += tuple([getattr(model, f) for f in id_field])
    result = _execute_query(query, parameters=parameters)
    return result == 1


def delete_data_by_id(*, table_name: str, id_field: tuple | str, id_value: int | str | tuple) -> bool:
    """
    Delete data from a table by ID.

    Args:
        table_name (str): The name of the table to delete data from.
        id_field (tuple | str): The field(s) representing the ID.
        id_value (int | str | tuple): The value(s) of the ID to delete.

    Returns:
        bool: True if the deletion was successful, False otherwise.
    """

    if not isinstance(id_field, tuple):
        id_field=(id_field, )
    query = f"""
        DELETE FROM {table_name}
        WHERE
            {' AND '.join([f'{f} = ?' for f in id_field])};
    """
    if not isinstance(id_value, tuple):
        id_value=(id_value, )
    result = _execute_query(query, parameters=id_value)

    return result == 1


def extract_create_stmts_objects(sql_file_path: str, object_type: str) -> list[str]:
    """
    Extract the CREATE statements objects from a SQL file.

    Args:
        sql_file_path (str): The path to the SQL file.
        object_type (str): The type of objects to extract from the SQL file.

    Returns:
        list: A list of dictionaries containing the objects.
    """

    try:
        with open(sql_file_path, "r") as f:
            sql = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {sql_file_path}")

    re_template = fr"CREATE\s+{object_type}\s+(IF\s+NOT\s+EXISTS\s+)*(\S+)"
    pattern = re.compile(re_template)
    result = []
    for m in pattern.finditer(sql):
        result.append(m.group(2))

    return result
