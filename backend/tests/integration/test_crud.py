import pytest

from app.db.crud.utils import insert_data_from_model
from app.models import AssetClass


def test_insert_data_from_model():
    asset_class = AssetClass(class_id=10, class_name="Test")
    with pytest.raises(ValueError):
        insert_data_from_model(table_name="asset_classes", id_field=("class_id", ), model=asset_class)
