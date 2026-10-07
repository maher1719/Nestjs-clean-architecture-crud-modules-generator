from typing import Any, Dict

Field = Dict[str, Any]
Relation = Dict[str, Any]


def ts_type(field: Field) -> str:
    field_type = str(field.get("type", "string")).lower()

    if field_type in {"uuid", "string", "text"}:
        return "string"
    if field_type in {"number", "int", "integer", "float", "decimal"}:
        return "number"
    if field_type == "boolean":
        return "boolean"
    if field_type in {"date", "datetime", "timestamp"}:
        return "Date"
    return "string"


def typeorm_type(field_type: str) -> str:
    field_type = str(field_type).lower()

    if field_type == "uuid":
        return "uuid"
    if field_type == "text":
        return "text"
    if field_type in {"number", "int", "integer", "float", "decimal"}:
        return "numeric"
    if field_type == "boolean":
        return "boolean"
    if field_type in {"date", "datetime", "timestamp"}:
        return "timestamptz"
    return "varchar"
