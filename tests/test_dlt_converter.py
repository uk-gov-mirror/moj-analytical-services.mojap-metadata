import pytest
import mojap_metadata
from mojap_metadata.metadata.metadata import Metadata
import mojap_metadata.converters.dlt_converter as dlt_convert

# test 1: basic type conversion from MOJAP to DLT types

def test_basic_conversion():
    # input schema with known MOJAP types
    input_schema = {
        "name": "test_table",
        "columns": [
            {"name": "id", "type": "int64"},
            {"name": "name", "type": "string"},
            {"name": "created_at", "type": "datetime"}
        ]
    }

    # expected output after conversion to DLT compatible types
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

    # run the conversion and assert the result matches expected output
    #metadata = Metadata.from_dict(input_schema)
    #result = metadata.to_dlt_schema()
    input_mojap_md = Metadata.from_dict(input_schema)
    result = dlt_convert.convert_metadata_to_dlt(input_mojap_md)

    assert result == expected_output


# test 2: unknown type should default to 'text' and print a warning
def test_unknown_type_defaults_to_text(capfd):
    # input schema with an unknown type
    input_schema = {
        "name": "test_table",
        "columns": [
            {"name": "custom_field", "type": "custom_type"}
        ]
    }

    # run the conversion and assert the result matches expected output
    #metadata = Metadata.from_dict(input_schema)
    #result = metadata.to_dlt_schema()
    input_mojap_md = Metadata.from_dict(input_schema)
    result = dlt_convert.convert_metadata_to_dlt(input_mojap_md)

    # assert that the unknown type was defaulted to 'text'
    assert result["tables"]["test_table"]["columns"]["custom_field"]["type"] == "text"

    # capture printed output and check for warning message
    out, _ = capfd.readouterr()
    assert "type : custom_type not found in type map" in out


# test 3: extra fields in column definitions should be preserved
def test_preserves_extra_fields():
    # input schema with additional metadata in columns
    input_schema = {
        "name": "test_table",
        "columns": [
            {"name": "id", "type": "int64", "nullable": False, "description": "Primary key"}
        ]
    }

    # run the conversion
    #metadata = Metadata.from_dict(input_schema)
    #result = metadata.to_dlt_schema()
    input_mojap_md = Metadata.from_dict(input_schema)
    result = dlt_convert.convert_metadata_to_dlt(input_mojap_md)

    # assert type conversion
    assert result["tables"]["test_table"]["columns"]["id"]["type"] == "bigint"

    # assert extra fields are preserved
    assert result["tables"]["test_table"]["columns"]["id"]["nullable"] is False
    assert result["tables"]["test_table"]["columns"]["id"]["description"] == "Primary key"


# test 4: schema with no columns should return an empty columns dict
def test_empty_columns():
    # input schema with no columns
    input_schema = {
        "name": "empty_table",
        "columns": []
    }

    # expected output with empty columns
    expected_output = {
        "name": "empty_table",
        "tables": {
            "empty_table": {
                "columns": {},
                "resource": "empty_table"
            }
        }
    }

    # run the conversion and assert the result matches expected output
    #metadata = Metadata.from_dict(input_schema)
    #result = metadata.to_dlt_schema()
    input_mojap_md = Metadata.from_dict(input_schema)
    result = dlt_convert.convert_metadata_to_dlt(input_mojap_md)
    assert result == expected_output
