from __future__ import annotations

import re
from typing import Any


ALLOWED_ON_DELETE = {
    "restrict",
    "cascade",
    "set-null",
    "no-action",
}

_ON_DELETE_TO_ORM = {
    "restrict": "RESTRICT",
    "cascade": "CASCADE",
    "set-null": "SET NULL",
    "no-action": "NO ACTION",
}


def kebab_case(value: str) -> str:
    value = re.sub(r"(?<!^)(?=[A-Z])", "-", value)
    value = re.sub(r"[^A-Za-z0-9]+", "-", value)
    return value.strip("-").lower()


def validate_mapping(
    relation: dict[str, Any],
    required_fields: set[str],
) -> None:
    missing = required_fields - relation.keys()
    if missing:
        raise ValueError(
            "Missing required relation fields: "
            + ", ".join(sorted(missing))
        )


def validate_on_delete(relation: dict[str, Any]) -> None:
    on_delete = relation.get("onDelete", "restrict")
    if on_delete not in ALLOWED_ON_DELETE:
        raise ValueError(
            f"Unsupported onDelete '{on_delete}'. "
            f"Expected one of: {', '.join(sorted(ALLOWED_ON_DELETE))}."
        )


def orm_on_delete(relation: dict[str, Any]) -> str:
    return _ON_DELETE_TO_ORM[relation.get("onDelete", "restrict")]


def validate_nullable(relation: dict[str, Any]) -> None:
    nullable = relation.get("nullable", False)
    if not isinstance(nullable, bool):
        raise ValueError("'nullable' must be a boolean.")


def build_import_path(
    target: str,
    target_module: str,
    current_module: str,
) -> str:
    target_kebab = kebab_case(target)
    if target_module and target_module != current_module:
        return (
            f"../../../../{target_module}"
            f"/infrastructure/persistence/typeorm/"
            f"{target_kebab}.orm-entity"
        )
    return f"./{target_kebab}.orm-entity"
