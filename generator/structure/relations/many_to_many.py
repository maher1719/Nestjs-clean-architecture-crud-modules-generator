from __future__ import annotations

from typing import Any

from .common import build_import_path, validate_mapping


RELATION_TYPE = "many-to-many"


def validate(relation: dict[str, Any]) -> None:
    required_fields = {
        "name",
        "type",
        "target",
        "targetModule",
        "joinTable",
        "joinColumn",
        "inverseJoinColumn",
    }
    validate_mapping(relation, required_fields)

    if relation["type"] != RELATION_TYPE:
        raise ValueError(f"Expected relation type '{RELATION_TYPE}'.")

    forbidden_fields = {"foreignKey", "nullable", "onDelete"}
    invalid = forbidden_fields & relation.keys()
    if invalid:
        raise ValueError(
            "many-to-many relations must not define: "
            + ", ".join(sorted(invalid))
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
    join_table = relation["joinTable"]
    join_column = relation["joinColumn"]
    inverse_join_column = relation["inverseJoinColumn"]
    target_entity = f"{target}OrmEntity"
    import_path = build_import_path(target, target_module, current_module)

    relation_code = (
        f"  @ManyToMany(() => {target_entity})\n"
        f"  @JoinTable({{\n"
        f"    name: '{join_table}',\n"
        f"    joinColumn: {{\n"
        f"      name: '{join_column}',\n"
        f"      referencedColumnName: 'id',\n"
        f"    }},\n"
        f"    inverseJoinColumn: {{\n"
        f"      name: '{inverse_join_column}',\n"
        f"      referencedColumnName: 'id',\n"
        f"    }},\n"
        f"  }})\n"
        f"  {relation_name}!: {target_entity}[];"
    )

    return {
        "relationImports": [
            f"import {{ {target_entity} }} from '{import_path}';"
        ],
        "ormRelations": [relation_code],
        "typeormImports": {"ManyToMany", "JoinTable"},
        "uniqueFields": set(),
    }
