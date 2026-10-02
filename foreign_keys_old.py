from __future__ import annotations

from typing import Any


ALLOWED_RELATION_TYPES = {
    "many-to-one",
    "one-to-many",
    "one-to-one",
    "many-to-many",
}

ALLOWED_ON_DELETE = {
    "restrict",
    "cascade",
    "set-null",
    "no-action",
}


def validate_foreign_keys(
    relations: Any,
) -> None:
    if relations is None:
        return

    if not isinstance(relations, list):
        raise ValueError(
            "'relations' must be a list."
        )

    for index, relation in enumerate(relations):
        if not isinstance(relation, dict):
            raise ValueError(
                f"Relation at index {index} "
                "must be a mapping."
            )

        required_fields = {
            "name",
            "type",
            "target",
            "targetModule",
            "foreignKey",
        }

        missing = (
            required_fields
            - relation.keys()
        )

        if missing:
            raise ValueError(
                f"Relation at index {index} "
                f"is missing: "
                f"{', '.join(sorted(missing))}"
            )

        relation_type = relation["type"]

        if relation_type not in ALLOWED_RELATION_TYPES:
            raise ValueError(
                f"Unsupported relation type "
                f"'{relation_type}'. "
                f"Currently supported: "
                f"{sorted(ALLOWED_RELATION_TYPES)}"
            )

        on_delete = relation.get(
            "onDelete",
            "restrict",
        )

        if on_delete not in ALLOWED_ON_DELETE:
            raise ValueError(
                f"Unsupported onDelete value "
                f"'{on_delete}'. "
                f"Allowed values: "
                f"{sorted(ALLOWED_ON_DELETE)}"
            )

        nullable = relation.get(
            "nullable",
            False,
        )

        if not isinstance(nullable, bool):
            raise ValueError(
                f"Relation '{relation['name']}': "
                "'nullable' must be boolean."
            )


def build_foreign_key_context(
    relations: Any,
    *,
    current_module:str,
) -> dict[str, Any]:
    if relations is None:
        relations = []

    validate_foreign_keys(relations)

    orm_imports: list[str] = []
    orm_relations: list[str] = []

    for relation in relations:
        target = relation["target"]
        target_module = relation["targetModule"]
        relation_name = relation["name"]
        foreign_key = relation["foreignKey"]

        nullable = relation.get(
            "nullable",
            False,
        )

        on_delete = relation.get(
            "onDelete",
            "restrict",
        )

        target_entity = (
            f"{target}OrmEntity"
        )

        import_path = (
            f"../../../../{target_module}"
            f"/infrastructure/persistence/"
            f"typeorm/"
            f"{_kebab_case(target)}.orm-entity"
        )

        orm_imports.append(
            f"import {{ {target_entity} }} "
            f"from '{import_path}';"
        )

        orm_on_delete = {
            "restrict": "RESTRICT",
            "cascade": "CASCADE",
            "set-null": "SET NULL",
            "no-action": "NO ACTION",
        }[on_delete]

        nullable_value = (
            "true"
            if nullable
            else "false"
        )

        orm_relations.append(
            f"""  @ManyToOne(
    () => {target_entity},
    {{
      nullable: {nullable_value},
      onDelete: '{orm_on_delete}',
    }},
  )
  @JoinColumn({{
    name: '{foreign_key}',
  }})
  {relation_name}!: {target_entity};"""
        )

    return {
        "relationImports": "\n".join(
            orm_imports
        ),
        "ormRelations": "\n\n".join(
            orm_relations
        ),
        "hasRelations": bool(relations),
    }


def _kebab_case(value: str) -> str:
    import re

    value = re.sub(
        r"([a-z0-9])([A-Z])",
        r"\1-\2",
        value,
    )

    value = re.sub(
        r"[_\s]+",
        "-",
        value,
    )

    return value.lower()