import pytest
from mojap_metadata.metadata.metadata import Metadata
#from mojap_metadata.metadata.metadata import to_dlt_schema


import pytest
from mojap_metadata.metadata.metadata import Metadata

def test_basic_conversion():
    input_schema = {
        "name": "test_table",
        "columns": [
            {"name": "id", "type": "int64"},
            {"name": "name", "type": "string"},
            {"name": "created_at", "type": "datetime"}
        ]
    }

    expected_output = {
        "name": "test_table",
        "tables": {
            "test_table": {
                "columns": {
                    "id": {"type": "bigint"},
                    "name": {"type": "text"},
                    "created_at": {"type": "timestamp"}
                },
                "resource": "test_table"
            }
        }
    }

    metadata = Metadata.from_dict(input_schema)
    result = metadata.to_dlt_schema()

    assert result == expected_output


