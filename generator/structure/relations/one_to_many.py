from __future__ import annotations

from typing import Any

from .common import build_import_path, validate_mapping


RELATION_TYPE = "one-to-many"


def validate(relation: dict[str, Any]) -> None:
    required_fields = {
        "name",
        "type",
        "target",
        "targetModule",
        "mappedBy",
    }
    validate_mapping(relation, required_fields)

    if relation["type"] != RELATION_TYPE:
        raise ValueError(f"Expected relation type '{RELATION_TYPE}'.")

    if "foreignKey" in relation:
        raise ValueError(
            "one-to-many relations must not define 'foreignKey'. "
            "The foreign key belongs to the many-to-one side."
        )


def build(
    relation: dict[str, Any],
    *,
    current_module: str,
) -> dict[str, Any]:
    validate(relation)

    target = relation["target"]
    target_module = relation["targetModule"]
    relation_name = relation["name"]
    mapped_by = relation["mappedBy"]
    target_entity = f"{target}OrmEntity"
    import_path = build_import_path(target, target_module, current_module)

    relation_code = (
        f"  @OneToMany(\n"
        f"    () => {target_entity},\n"
        f"    (related) => related.{mapped_by},\n"
        f"  )\n"
        f"  {relation_name}!: {target_entity}[];"
    )

    return {
        "relationImports": [
            f"import {{ {target_entity} }} from '{import_path}';"
        ],
        "ormRelations": [relation_code],
        # FIXED: inverse side does NOT use JoinColumn
        "typeormImports": {"OneToMany"},
        "uniqueFields": set(),
    }
