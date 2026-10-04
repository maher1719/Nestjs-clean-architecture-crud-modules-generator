from typing import Any, Dict, List

from .naming import change_method_name, kebab_case

Field = Dict[str, Any]
Relation = Dict[str, Any]


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


def ts_type(field: Field) -> str:
    field_type = str(field.get("type", "string")).lower()

    if field_type in {"uuid", "string", "text"}:
        return "string"

    if field_type in {"number", "int", "integer", "float", "decimal"}:
        return "number"

    if field_type == "boolean":
        return "boolean"

    if field_type in {"date", "datetime", "timestamp"}:
        return "Date"

    return "string"


def typeorm_type(field_type: str) -> str:
    field_type = str(field_type).lower()

    if field_type == "uuid":
        return "uuid"

    if field_type == "text":
        return "text"

    if field_type in {"number", "int", "integer", "float", "decimal"}:
        return "numeric"

    if field_type == "boolean":
        return "boolean"

    if field_type in {"date", "datetime", "timestamp"}:
        return "timestamptz"

    return "varchar"


def build_entity_props(fields: List[Field]) -> str:
    lines = []

    for field in fields:
        name = field["name"]
        field_ts_type = ts_type(field)

        lines.append(f"  {name}: {field_ts_type};")

    return "\n".join(lines)


def build_create_entity_parameters(fields: List[Field]) -> str:
    lines = []

    for field in fields:
        name = field["name"]
        field_ts_type = ts_type(field)

        lines.append(f"    {name}: {field_ts_type},")

    return "\n".join(lines)


def build_create_entity_fields(fields: List[Field]) -> str:
    lines = []

    for field in fields:
        name = field["name"]

        lines.append(f"      {name},")

    return "\n".join(lines)


def build_create_command_parameters(fields: List[Field]) -> str:
    parts = []

    for field in fields:
        name = field["name"]
        field_ts_type = ts_type(field)

        parts.append(f"public readonly {name}: {field_ts_type}")

    return ", ".join(parts)


def build_create_handler_arguments(fields: List[Field]) -> str:
    parts = []

    for field in fields:
        name = field["name"]

        parts.append(f"command.{name}")

    return ", ".join(parts)


def build_create_controller_arguments(fields: List[Field]) -> str:
    lines = []

    for field in fields:
        name = field["name"]

        lines.append(f"      dto.{name},")

    return "\n".join(lines)


def build_update_command_parameters(fields: List[Field]) -> str:
    lines = []

    for field in fields:
        name = field["name"]
        field_ts_type = ts_type(field)

        lines.append(f"    public readonly {name}?: {field_ts_type},")

    return "\n".join(lines)


def build_update_controller_arguments(fields: List[Field]) -> str:
    lines = []

    for field in fields:
        name = field["name"]

        lines.append(f"      dto.{name},")

    return "\n".join(lines)


def build_update_methods(fields: List[Field]) -> str:
    blocks = []

    for field in fields:
        name = field["name"]
        field_ts_type = ts_type(field)
        method_name = change_method_name(name)

        block = [
            f"  {method_name}(value: {field_ts_type}): void {{",
            f"    this.props.{name} = value;",
            "    this.props.updatedAt = new Date();",
            "  }",
        ]

        blocks.append("\n".join(block))

    return "\n\n".join(blocks)


def build_getters(fields: List[Field]) -> str:
    lines = []

    def add_getter(name: str, getter_type: str) -> None:
        lines.append(f"  get {name}(): {getter_type} {{")
        lines.append(f"    return this.props.{name};")
        lines.append("  }")
        lines.append("")

    add_getter("id", "string")

    for field in fields:
        add_getter(field["name"], ts_type(field))

    add_getter("createdAt", "Date")
    add_getter("updatedAt", "Date")

    return "\n".join(lines).rstrip()


def build_update_handler_assignments(fields: List[Field]) -> str:
    blocks = []

    for field in fields:
        name = field["name"]
        method_name = change_method_name(name)

        block = [
            f"    if (command.{name} !== undefined) {{",
            f"      entity.{method_name}(command.{name});",
            "    }",
        ]

        blocks.append("\n".join(block))

    return "\n\n".join(blocks)


"""def build_create_dto_fields(fields: List[Field]) -> str:
    lines = []

    for field in fields:
        name = field["name"]
        field_ts_type = ts_type(field)

        lines.append(f"  {name}: {field_ts_type};")

    return "\n".join(lines)"""
# ----------------------------------------------------------------------
# Type mapping
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# Validator & Swagger helpers (ADD THESE TO fields.py)
# ----------------------------------------------------------------------



# ----------------------------------------------------------------------
# Validator & Swagger helpers
# ----------------------------------------------------------------------

def validator_name(field_type: str) -> str:
    mapping = {
        "string": "IsString",
        "number": "IsNumber",
        "boolean": "IsBoolean",
        "date": "IsDateString",
        "uuid": "IsUUID",
    }
    try:
        return mapping[field_type]
    except KeyError as exc:
        raise ValueError(f"No DTO validator for type '{field_type}'.") from exc


def swagger_property_options(field_type: str) -> str:
    mapping = {
        "string": "",
        "number": "type: Number",
        "boolean": "type: Boolean",
        "date": "type: String, format: 'date-time'",
        "uuid": "type: String, format: 'uuid'",
    }
    try:
        return mapping[field_type]
    except KeyError as exc:
        raise ValueError(f"No Swagger metadata for type '{field_type}'.") from exc


def build_validator_imports(fields: List[Field], *, required: bool) -> str:
    imports = {validator_name(str(field.get("type", "string")).lower()) for field in fields}
    imports.add("IsNotEmpty" if required else "IsOptional")
    return ",\n  ".join(sorted(imports))

# ----------------------------------------------------------------------
# FIXED DTO generators (Clean Indentation)
# ----------------------------------------------------------------------

def build_create_dto_fields(fields: List[Field]) -> str:
    result: list[str] = []
    for field in fields:
        name = field["name"]
        field_type = str(field.get("type", "string")).lower()
        type_name = ts_type(field)  # ← pass the whole dict!
        validator = validator_name(field_type)
        swagger_options = swagger_property_options(field_type)

        if swagger_options:
            api_property = f"@ApiProperty({{{swagger_options}, description: '{name}'}})"
        else:
            api_property = f"@ApiProperty({{ description: '{name}' }})"

        result.append(
            f"  {api_property}\n"
            f"  @{validator}()\n"
            f"  @IsNotEmpty()\n"
            f"  {name}!: {type_name};"
        )
    return "\n\n".join(result)

def build_update_dto_fields(fields: List[Field]) -> str:
    result: list[str] = []
    for field in fields:
        name = field["name"]
        field_type = str(field.get("type", "string")).lower()
        
        type_name = ts_type(field)
        validator = validator_name(field_type)
        swagger_options = swagger_property_options(field_type)
        
        if swagger_options:
            api_property = f"@ApiPropertyOptional({{{swagger_options}, description: '{name}'}})"
        else:
            api_property = f"@ApiPropertyOptional({{ description: '{name}' }})"
            
        result.append(
            f"  {api_property}\n"
            f"  @IsOptional()\n"
            f"  @{validator}()\n"
            f"  {name}?: {type_name};"
        )
    return "\n\n".join(result)

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

# ----------------------------------------------------------------------
# TypeORM imports (base + relation decorators, merged into ONE statement)
# ----------------------------------------------------------------------

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


# ----------------------------------------------------------------------
# ORM columns (relations are NO LONGER inlined here — they go to ${ormRelations})
# ----------------------------------------------------------------------

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

        # Unique comes from the field itself OR from a relation (one-to-one FK)
        if field.get("unique", False) or name in unique_fields:
            options.append("unique: true")

        options_string = "{ " + ", ".join(options) + " }"

        lines.append(f"  @Column({options_string})")
        lines.append(f"  {name}: {field_ts_type};")
        lines.append("")

    return "\n".join(lines).rstrip()

def build_replace_command_parameters(fields: List[Field]) -> str:
    return build_create_command_parameters(fields)

def build_replace_controller_arguments(fields: List[Field]) -> str:
    return build_create_controller_arguments(fields)

def build_replace_dto_fields(fields: List[Field]) -> str:
    return build_create_dto_fields(fields)

def build_field_context(fields: List[Field]) -> Dict[str, str]:
    return {
        "entityProps": build_entity_props(fields),
        "createEntityParameters": build_create_entity_parameters(fields),
        "createEntityFields": build_create_entity_fields(fields),
        "createCommandParameters": build_create_command_parameters(fields),
        "createHandlerArguments": build_create_handler_arguments(fields),
        "createControllerArguments": build_create_controller_arguments(fields),
        "updateCommandParameters": build_update_command_parameters(fields),
        "updateControllerArguments": build_update_controller_arguments(fields),
        "updateMethods": build_update_methods(fields),
        "getters": build_getters(fields),
        "updateHandlerAssignments": build_update_handler_assignments(fields),
        "createValidatorImports": build_validator_imports(fields, required=True),
        "updateValidatorImports": build_validator_imports(fields, required=False),
        "createDtoFields": build_create_dto_fields(fields),
        "updateDtoFields": build_update_dto_fields(fields),
        "ormToDomainFields": build_orm_to_domain_fields(fields),
        "domainToOrmFields": build_domain_to_orm_fields(fields),
        "replaceCommandParameters": build_replace_command_parameters(fields),
        "replaceControllerArguments": build_replace_controller_arguments(fields),
        "replaceDtoFields": build_replace_dto_fields(fields),
        "replaceValidatorImports": build_validator_imports(fields, required=True),
    }
