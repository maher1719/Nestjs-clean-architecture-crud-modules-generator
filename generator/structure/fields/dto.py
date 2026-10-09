from typing import List

from .types import Field, ts_type


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
    imports = {
        validator_name(str(field.get("type", "string")).lower())
        for field in fields
    }
    imports.add("IsNotEmpty" if required else "IsOptional")
    return ",\n  ".join(sorted(imports))

def build_replace_dto_fields(fields: List[Field]) -> str:
    # Full replacement -> same shape as Create DTO (required, @IsNotEmpty)
    return build_create_dto_fields(fields)


def build_create_dto_fields(fields: List[Field]) -> str:
    result: List[str] = []
    for field in fields:
        name = field["name"]
        field_type = str(field.get("type", "string")).lower()
        type_name = ts_type(field)
        validator = validator_name(field_type)
        swagger_options = swagger_property_options(field_type)

        if swagger_options:
            api_property = (
                f"@ApiProperty({{{swagger_options}, description: '{name}'}})"
            )
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
    result: List[str] = []
    for field in fields:
        name = field["name"]
        field_type = str(field.get("type", "string")).lower()
        type_name = ts_type(field)
        validator = validator_name(field_type)
        swagger_options = swagger_property_options(field_type)

        if swagger_options:
            api_property = (
                f"@ApiPropertyOptional({{{swagger_options}, description: '{name}'}})"
            )
        else:
            api_property = f"@ApiPropertyOptional({{ description: '{name}' }})"

        result.append(
            f"  {api_property}\n"
            f"  @IsOptional()\n"
            f"  @{validator}()\n"
            f"  {name}?: {type_name};"
        )
    return "\n\n".join(result)

def build_list_filter_dto_fields(fields: List[Field]) -> str:
    lines = []
    for field in fields:
        if not field.get("filterable", False):
            continue
        name = field["name"]
        field_type = str(field.get("type", "string")).lower()
        type_name = ts_type(field)
        validator = validator_name(field_type)
        swagger_options = swagger_property_options(field_type)
        api = (
            f"@ApiPropertyOptional({{{swagger_options}}})"
            if swagger_options
            else "@ApiPropertyOptional()"
        )
        lines.append(
            f"  {api}\n"
            f"  @IsOptional()\n"
            f"  @{validator}()\n"
            f"  {name}?: {type_name};\n"
        )
    return "\n".join(lines)


def build_sortable_fields_list(fields: List[Field]) -> str:
    names = ["'id'", "'createdAt'", "'updatedAt'"]
    for field in fields:
        if field.get("sortable", False):
            names.append(f"'{field['name']}'")
    return ", ".join(names)


def build_list_filter_validator_imports(fields: List[Field]) -> str:
    imports = set()
    for field in fields:
        if field.get("filterable", False):
            imports.add(validator_name(str(field.get("type", "string")).lower()))
    if not imports:
        return ""
    return ",\n".join(f"  {i}" for i in sorted(imports)) + ","


def build_list_filter_assignments(fields: List[Field]) -> str:
    lines = []
    for field in fields:
        if not field.get("filterable", False):
            continue
        name = field["name"]
        lines.append(
            f"  if (query.{name} !== undefined) filters['{name}'] = query.{name};"
        )
    return "\n".join(lines)
