from typing import List

from .types import Field


def build_orm_to_domain_fields(fields: List[Field]) -> str:
    lines = []
    for field in fields:
        name = field["name"]
        lines.append(f"      {name}: orm.{name},")
    return "\n".join(lines)


def build_domain_to_orm_fields(fields: List[Field]) -> str:
    lines = []
    for field in fields:
        name = field["name"]
        lines.append(f"    orm.{name} = entity.{name};")
    return "\n".join(lines)
