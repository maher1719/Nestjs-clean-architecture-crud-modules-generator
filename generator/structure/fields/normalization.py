from typing import Any, List

from .types import Field, Relation


EXCLUDED_FIELD_NAMES = {
    "id",
    "createdAt",
    "updatedAt",
}


def normalize_fields(fields: Any) -> List[Field]:
    if not fields:
        return []
    if isinstance(fields, dict):
        fields = [fields]

    normalized: List[Field] = []
    for field in fields:
        if not isinstance(field, dict):
            continue
        if not field.get("name"):
            continue
        if field["name"] in EXCLUDED_FIELD_NAMES:
            continue
        normalized.append(field)
    return normalized


def normalize_relations(relations: Any) -> List[Relation]:
    if not relations:
        return []
    if isinstance(relations, dict):
        relations = [relations]

    normalized: List[Relation] = []
    for relation in relations:
        if not isinstance(relation, dict):
            continue
        if not relation.get("name"):
            continue
        normalized.append(relation)
    return normalized
