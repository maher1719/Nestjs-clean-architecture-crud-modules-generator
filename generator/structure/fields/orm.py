from typing import List

from .types import Field, ts_type, typeorm_type


BASE_TYPEORM_IMPORTS = [
    "Column",
    "CreateDateColumn",
    "Entity",
    "PrimaryColumn",
    "UpdateDateColumn",
]


def build_typeorm_imports(relation_decorators) -> str:
    merged = sorted(set(BASE_TYPEORM_IMPORTS) | set(relation_decorators or []))
    lines = ["import {"]
    for item in merged:
        lines.append(f"  {item},")
    lines.append("} from 'typeorm';")
    return "\n".join(lines)


def build_orm_columns(fields: List[Field], *, unique_fields=None) -> str:
    if unique_fields is None:
        unique_fields = set()

    lines = []
    for field in fields:
        name = field["name"]
        field_ts_type = ts_type(field)
        field_type = str(field.get("type", "string")).lower()

        options = []
        orm_type = field.get("orm_type")
        if orm_type:
            options.append(f"type: '{orm_type}'")
        else:
            options.append(f"type: '{typeorm_type(field_type)}'")

        length = field.get("length")
        if length:
            options.append(f"length: {length}")

        nullable = bool(field.get("nullable", False))
        options.append(f"nullable: {str(nullable).lower()}")

        if field.get("unique", False) or name in unique_fields:
            options.append("unique: true")

        options_string = "{ " + ", ".join(options) + " }"
        lines.append(f"  @Column({options_string})")
        lines.append(f"  {name}: {field_ts_type};")
        lines.append("")

    return "\n".join(lines).rstrip()
