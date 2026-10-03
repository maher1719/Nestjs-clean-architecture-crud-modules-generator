from pathlib import Path
from typing import Any, Dict

import yaml


ALLOWED_OPERATIONS = {
    "create",
    "list",
    "get",
    "update",
    "delete",
    "replace",
    "patch",
}


def load_config(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    validate_config(config)

    return config


def validate_config(config: Dict[str, Any]) -> None:
    if not isinstance(config, dict):
        raise ValueError("YAML root must be a dictionary/object.")

    if "module" not in config:
        raise ValueError("Missing required YAML key: module")

    if "entity" not in config:
        raise ValueError("Missing required YAML key: entity")

    if not isinstance(config["module"], str):
        raise ValueError("YAML key 'module' must be a string.")

    entity = config["entity"]

    if not isinstance(entity, dict):
        raise ValueError("YAML key 'entity' must be an object.")

    if "name" not in entity:
        raise ValueError("Missing required YAML key: entity.name")

    if "table" not in entity:
        raise ValueError("Missing required YAML key: entity.table")

    if "fields" not in entity:
        raise ValueError("Missing required YAML key: entity.fields")

    if not isinstance(entity["name"], str):
        raise ValueError("YAML key 'entity.name' must be a string.")

    if not isinstance(entity["table"], str):
        raise ValueError("YAML key 'entity.table' must be a string.")

    fields = entity["fields"]

    if not isinstance(fields, list):
        raise ValueError("YAML key 'entity.fields' must be a list.")

    for index, field in enumerate(fields):
        if not isinstance(field, dict):
            raise ValueError(f"Field at index {index} must be an object.")

        if "name" not in field:
            raise ValueError(f"Field at index {index} is missing required key: name")

    relations = config.get("relations")

    if relations is not None and not isinstance(relations, list):
        raise ValueError("YAML key 'relations' must be a list.")

    operations = config.get("operations")

    if operations is not None:
        if not isinstance(operations, list):
            raise ValueError("YAML key 'operations' must be a list.")

        normalized_operations = {
            str(operation).lower() for operation in operations
        }

        invalid_operations = normalized_operations - ALLOWED_OPERATIONS

        if invalid_operations:
            raise ValueError(
                "Invalid operations: "
                f"{', '.join(sorted(invalid_operations))}. "
                f"Allowed operations are: {', '.join(sorted(ALLOWED_OPERATIONS))}."
            )
