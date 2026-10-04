from __future__ import annotations

from typing import Any

from .common import (
    build_import_path,
    orm_on_delete,
    validate_mapping,
    validate_nullable,
    validate_on_delete,
)


RELATION_TYPE = "many-to-one"


def validate(relation: dict[str, Any]) -> None:
    required_fields = {
        "name",
        "type",
        "target",
        "targetModule",
        "foreignKey",
    }
    validate_mapping(relation, required_fields)

    if relation["type"] != RELATION_TYPE:
        raise ValueError(f"Expected relation type '{RELATION_TYPE}'.")

    validate_nullable(relation)
    validate_on_delete(relation)


def build(
    relation: dict[str, Any],
    *,
    current_module: str,
) -> dict[str, Any]:
    validate(relation)

    target = relation["target"]
    target_module = relation["targetModule"]
    relation_name = relation["name"]
    foreign_key = relation["foreignKey"]
    target_entity = f"{target}OrmEntity"
    import_path = build_import_path(target, target_module, current_module)
    nullable = str(relation.get("nullable", False)).lower()

    relation_code = (
        f"  @ManyToOne(\n"
        f"    () => {target_entity},\n"
        f"    {{\n"
        f"      nullable: {nullable},\n"
        f"      onDelete: '{orm_on_delete(relation)}',\n"
        f"    }},\n"
        f"  )\n"
        f"  @JoinColumn({{ name: '{foreign_key}' }})\n"
        f"  {relation_name}!: {target_entity};"
    )

    return {
        "relationImports": [
            f"import {{ {target_entity} }} from '{import_path}';"
        ],
        "ormRelations": [relation_code],
        "typeormImports": {"ManyToOne", "JoinColumn"},
        "uniqueFields": set(),
    }
