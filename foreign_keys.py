from __future__ import annotations

from typing import Any

from relations import (
    many_to_many,
    many_to_one,
    one_to_many,
    one_to_one,
)


RELATION_BUILDERS = {
    "many-to-one": many_to_one,
    "one-to-many": one_to_many,
    "one-to-one": one_to_one,
    "many-to-many": many_to_many,
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
                f"must be a mapping."
            )

        if "type" not in relation:
            raise ValueError(
                f"Relation at index {index} "
                f"is missing 'type'."
            )

        relation_type = relation["type"]

        if relation_type not in RELATION_BUILDERS:
            raise ValueError(
                f"Unsupported relation type "
                f"'{relation_type}'. "
                f"Expected one of: "
                f"{', '.join(sorted(RELATION_BUILDERS))}."
            )


def build_foreign_key_context(
    relations: Any,
    *,
    current_module: str,
) -> dict[str, Any]:

    if relations is None:
        relations = []

    validate_foreign_keys(relations)

    relation_imports: list[str] = []
    orm_relations: list[str] = []
    typeorm_imports: set[str] = set()
    unique_fields: set[str] = set()

    for relation in relations:
        relation_type = relation["type"]

        builder = RELATION_BUILDERS[
            relation_type
        ]

        result = builder.build(
            relation,
            current_module=current_module,
        )

        relation_imports.extend(
            result["relationImports"]
        )

        orm_relations.extend(
            result["ormRelations"]
        )

        typeorm_imports.update(
            result["typeormImports"]
        )

        unique_fields.update(
            result["uniqueFields"]
        )

    return {
        "relationImports": "\n".join(
            relation_imports
        ),
        "ormRelations": "\n\n".join(
            orm_relations
        ),
        "relationTypeOrmImports": ",\n  ".join(
            sorted(typeorm_imports)
        ),
        "uniqueFields": unique_fields,
        "hasRelations": bool(relations),
    }