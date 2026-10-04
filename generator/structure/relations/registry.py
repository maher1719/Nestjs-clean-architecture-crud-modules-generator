from __future__ import annotations

from typing import Any

from . import many_to_many
from . import many_to_one
from . import one_to_many
from . import one_to_one


RELATION_BUILDERS = {
    "many-to-one": many_to_one,
    "one-to-many": one_to_many,
    "one-to-one": one_to_one,
    "many-to-many": many_to_many,
}


def validate_relations(relations: Any) -> None:
    if relations is None:
        return
    if not isinstance(relations, list):
        raise ValueError("'relations' must be a list.")

    for index, relation in enumerate(relations):
        if not isinstance(relation, dict):
            raise ValueError(f"Relation at index {index} must be a mapping.")
        if "type" not in relation:
            raise ValueError(f"Relation at index {index} is missing 'type'.")

        relation_type = relation["type"]
        if relation_type not in RELATION_BUILDERS:
            raise ValueError(
                f"Unsupported relation type '{relation_type}'. "
                f"Expected one of: {', '.join(sorted(RELATION_BUILDERS))}."
            )


def build_relations_context(
    relations: Any,
    *,
    current_module: str,
    current_entity: str = "",
) -> dict[str, Any]:
    if relations is None:
        relations = []

    validate_relations(relations)

    relation_imports: list[str] = []
    orm_relations: list[str] = []
    typeorm_imports: set[str] = set()
    unique_fields: set[str] = set()

    # The ORM class being generated in the current file. Any relation that
    # imports this class is a self-reference (e.g. Comment.parent -> Comment)
    # and must NOT emit an import, since the class is already in scope.
    current_orm_class = (
        f"{current_entity}OrmEntity" if current_entity else None
    )

    for relation in relations:
        builder = RELATION_BUILDERS[relation["type"]]
        result = builder.build(relation, current_module=current_module)

        # Skip self-referential imports, keep everything else
        for import_line in result["relationImports"]:
            if current_orm_class and current_orm_class in import_line:
                continue
            relation_imports.append(import_line)

        orm_relations.extend(result["ormRelations"])
        typeorm_imports.update(result["typeormImports"])
        unique_fields.update(result["uniqueFields"])

    # Deduplicate identical imports while preserving order
    # (e.g. two relations pointing at the same target entity)
    relation_imports = list(dict.fromkeys(relation_imports))

    return {
        "relationImports": "\n".join(relation_imports),
        "ormRelations": "\n\n".join(orm_relations),
        "relationTypeOrmImports": sorted(typeorm_imports),
        "uniqueFields": unique_fields,
        "hasRelations": bool(relations),
    }