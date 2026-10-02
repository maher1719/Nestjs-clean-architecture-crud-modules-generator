from __future__ import annotations

from foreign_keys import build_foreign_key_context

import argparse
import re
from pathlib import Path
from typing import Any

import yaml


BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
BACKEND_SRC_DIR = BASE_DIR.parent.parent / "src"
MODULES_DIR = BACKEND_SRC_DIR / "modules"


ALLOWED_TYPES = {
    "string",
    "number",
    "boolean",
    "date",
    "uuid",
}

ALLOWED_OPERATIONS = {
    "create",
    "list",
    "get",
    "update",
    "delete",
}

PLACEHOLDER_PATTERN = re.compile(
    r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}"
)


# ----------------------------------------------------------------------
# Naming
# ----------------------------------------------------------------------


def pascal_case(value: str) -> str:
    parts = re.split(
        r"[-_\s]+",
        value,
    )

    return "".join(
        part[:1].upper() + part[1:]
        for part in parts
        if part
    )


def camel_case(value: str) -> str:
    pascal = pascal_case(value)

    if not pascal:
        return ""

    return pascal[0].lower() + pascal[1:]


def kebab_case(value: str) -> str:
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


# ----------------------------------------------------------------------
# Type mapping
# ----------------------------------------------------------------------


def typescript_type(type_name: str) -> str:
    mapping = {
        "string": "string",
        "number": "number",
        "boolean": "boolean",
        "date": "Date",
        "uuid": "string",
    }

    try:
        return mapping[type_name]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported field type: {type_name}"
        ) from exc


def build_typeorm_imports(
    relation_imports: str,
) -> str:
    base_imports = [
        "Entity",
        "Column",
        "PrimaryColumn",
        "CreateDateColumn",
        "UpdateDateColumn",
    ]

    if relation_imports:
        imports = (
            base_imports
            + relation_imports.split(",\n  ")
        )
    else:
        imports = base_imports

    imports = sorted(set(imports))

    return (
        "import {\n"
        + "\n".join(
            f"  {item},"
            for item in imports
        )
        + "\n"
        + "} from 'typeorm';"
    )


def orm_column(
    field: dict[str, Any],
    *,
    unique: bool = False,
) -> str:
    name = field["name"]
    field_type = field["type"]

    if field_type == "string":
        options = (
            "type: 'varchar', "
            "length: 255"
        )

    elif field_type == "number":
        options = "type: 'integer'"

    elif field_type == "boolean":
        options = "type: 'boolean'"

    elif field_type == "date":
        options = "type: 'timestamptz'"

    elif field_type == "uuid":
        options = "type: 'uuid'"

    else:
        raise ValueError(
            f"Unsupported field type '{field_type}'."
        )

    if unique:
        options += ", unique: true"

    return (
        f"  @Column({{{options}}})\n"
        f"  {name}!: "
        f"{typescript_type(field_type)};"
    )


# ----------------------------------------------------------------------
# YAML validation
# ----------------------------------------------------------------------


def validate_config(
    config: dict[str, Any],
) -> None:
    if not isinstance(config, dict):
        raise ValueError(
            "Configuration must be a YAML mapping."
        )

    module = config.get("module")

    if not isinstance(module, str) or not module.strip():
        raise ValueError(
            "'module' must be a non-empty string."
        )

    entity = config.get("entity")

    if not isinstance(entity, dict):
        raise ValueError(
            "'entity' must be a mapping."
        )

    entity_name = entity.get("name")
    table_name = entity.get("table")

    if (
        not isinstance(entity_name, str)
        or not entity_name.strip()
    ):
        raise ValueError(
            "'entity.name' must be a non-empty string."
        )

    if (
        not isinstance(table_name, str)
        or not table_name.strip()
    ):
        raise ValueError(
            "'entity.table' must be a non-empty string."
        )

    fields = entity.get("fields")

    if not isinstance(fields, list):
        raise ValueError(
            "'entity.fields' must be a list."
        )

    operations = config.get("operations")

    if not isinstance(operations, list):
        raise ValueError(
            "'operations' must be a list."
        )

    unknown_operations = (
        set(operations) - ALLOWED_OPERATIONS
    )

    if unknown_operations:
        raise ValueError(
            "Unknown operations: "
            f"{sorted(unknown_operations)}"
        )

    seen_names: set[str] = set()

    reserved_names = {
        "id",
        "createdAt",
        "updatedAt",
    }

    for field in fields:
        if not isinstance(field, dict):
            raise ValueError(
                "Every entity field must be a mapping."
            )

        name = field.get("name")
        field_type = field.get("type")

        if (
            not isinstance(name, str)
            or not name.strip()
        ):
            raise ValueError(
                "Every field requires a "
                "non-empty string 'name'."
            )

        if name in reserved_names:
            raise ValueError(
                f"Field '{name}' is reserved."
            )

        if name in seen_names:
            raise ValueError(
                f"Duplicate field name: '{name}'."
            )

        seen_names.add(name)

        if field_type not in ALLOWED_TYPES:
            raise ValueError(
                f"Unsupported field type "
                f"'{field_type}' for field "
                f"'{name}'. Allowed types: "
                f"{sorted(ALLOWED_TYPES)}"
            )


# ----------------------------------------------------------------------
# Field generators
# ----------------------------------------------------------------------


def build_entity_props(
    fields: list[dict[str, Any]],
) -> str:
    return "\n".join(
        f"  {field['name']}: "
        f"{typescript_type(field['type'])};"
        for field in fields
    )


def build_create_entity_parameters(
    fields: list[dict[str, Any]],
) -> str:
    return "\n".join(
        f"    {field['name']}: "
        f"{typescript_type(field['type'])},"
        for field in fields
    )


def build_create_entity_fields(
    fields: list[dict[str, Any]],
) -> str:
    return "\n".join(
        f"      {field['name']},"
        for field in fields
    )


def build_getters(
    fields: list[dict[str, Any]],
) -> str:
    standard_fields = [
        ("id", "string"),
        ("createdAt", "Date"),
        ("updatedAt", "Date"),
    ]

    all_fields = standard_fields + [
        (
            field["name"],
            typescript_type(field["type"]),
        )
        for field in fields
    ]

    getters: list[str] = []

    for name, type_name in all_fields:
        method_name = (
            f"get{pascal_case(name)}"
        )

        getters.append(
            f"""  {method_name}(): {type_name} {{
    return this.props.{name};
  }}"""
        )

    return "\n\n".join(getters)


def build_update_methods(
    fields: list[dict[str, Any]],
) -> str:
    methods: list[str] = []

    for field in fields:
        name = field["name"]

        type_name = typescript_type(
            field["type"]
        )

        method_name = (
            f"update{pascal_case(name)}"
        )

        methods.append(
            f"""  {method_name}(
    value: {type_name},
  ): void {{
    this.props.{name} = value;
    this.props.updatedAt = new Date();
  }}"""
        )

    return "\n\n".join(methods)


# ----------------------------------------------------------------------
# Command generators
# ----------------------------------------------------------------------


def build_create_command_parameters(
    fields: list[dict[str, Any]],
) -> str:
    return "\n".join(
        f"    public readonly {field['name']}: "
        f"{typescript_type(field['type'])},"
        for field in fields
    )


def build_create_handler_fields(
    fields: list[dict[str, Any]],
) -> str:
    return "\n".join(
        f"      command.{field['name']},"
        for field in fields
    )


def build_create_handler_test_arguments(
    fields: list[dict[str, Any]],
) -> str:
    values = {
        "string": "'value'",
        "number": "1",
        "boolean": "true",
        "date": "new Date()",
        "uuid": (
            "'550e8400-e29b-41d4-a716-446655440000'"
        ),
    }

    return "\n".join(
        f"      {values[field['type']]},"
        for field in fields
    )


def build_update_command_parameters(
    fields: list[dict[str, Any]],
) -> str:
    return "\n".join(
        f"    public readonly {field['name']}?: "
        f"{typescript_type(field['type'])},"
        for field in fields
    )


def build_update_domain_operation(
    fields: list[dict[str, Any]],
    entity_name: str,
) -> str:
    operations: list[str] = []

    for field in fields:
        name = field["name"]

        method_name = (
            f"update{pascal_case(name)}"
        )

        operations.append(
            f"""    if (command.{name} !== undefined) {{
      {entity_name}.{method_name}(
        command.{name},
      );
    }}"""
        )

    return "\n\n".join(operations)


# ----------------------------------------------------------------------
# Persistence generators
# ----------------------------------------------------------------------


def build_persistence_to_domain_fields(
    fields: list[dict[str, Any]],
) -> str:
    all_fields = [
        "id",
        *(field["name"] for field in fields),
        "createdAt",
        "updatedAt",
    ]

    return ",\n".join(
        f"      {field}: entity.{field}"
        for field in all_fields
    )


def build_domain_to_persistence_fields(
    fields: list[dict[str, Any]],
    entity_name: str,
) -> str:
    all_fields = [
        "id",
        *(field["name"] for field in fields),
        "createdAt",
        "updatedAt",
    ]

    return "\n".join(
        f"    entity.{field} = "
        f"{entity_name}.get{pascal_case(field)}();"
        for field in all_fields
    )


def build_orm_columns(
    fields: list[dict[str, Any]],
    *,
    unique_fields: set[str],
) -> str:
    columns = []

    for field in fields:
        columns.append(
            orm_column(
                field,
                unique=field["name"] in unique_fields,
            )
        )

    return "\n\n".join(columns)


# ----------------------------------------------------------------------
# DTO generators
# ----------------------------------------------------------------------


def validator_name(
    field_type: str,
) -> str:
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
        raise ValueError(
            f"No DTO validator for type "
            f"'{field_type}'."
        ) from exc


def build_validator_imports(
    fields: list[dict[str, Any]],
    *,
    required: bool,
) -> str:
    imports = {
        validator_name(field["type"])
        for field in fields
    }

    imports.add(
        "IsNotEmpty"
        if required
        else "IsOptional"
    )

    return ",\n  ".join(
        sorted(imports)
    )


def build_create_dto_fields(
    fields: list[dict[str, Any]],
) -> str:
    result: list[str] = []

    for field in fields:
        name = field["name"]

        type_name = typescript_type(
            field["type"]
        )

        validator = validator_name(
            field["type"]
        )

        result.append(
            f"""  @{validator}()
  @IsNotEmpty()
  {name}!: {type_name};"""
        )

    return "\n\n".join(result)


def build_update_dto_fields(
    fields: list[dict[str, Any]],
) -> str:
    result: list[str] = []

    for field in fields:
        name = field["name"]

        type_name = typescript_type(
            field["type"]
        )

        validator = validator_name(
            field["type"]
        )

        result.append(
            f"""  @IsOptional()
  @{validator}()
  {name}?: {type_name};"""
        )

    return "\n\n".join(result)


# ----------------------------------------------------------------------
# Controller generators
# ----------------------------------------------------------------------


def build_create_controller_arguments(
    fields: list[dict[str, Any]],
) -> str:
    return "\n".join(
        f"      dto.{field['name']},"
        for field in fields
    )


def build_update_controller_arguments(
    fields: list[dict[str, Any]],
) -> str:
    return "\n".join(
        f"      dto.{field['name']},"
        for field in fields
    )


# ----------------------------------------------------------------------
# Template rendering
# ----------------------------------------------------------------------


def render_template(
    template: str,
    context: dict[str, Any],
) -> str:
    placeholders = set(
        PLACEHOLDER_PATTERN.findall(template)
    )

    missing = sorted(
        placeholder
        for placeholder in placeholders
        if placeholder not in context
    )

    if missing:
        raise ValueError(
            "Unknown template variable(s): "
            + ", ".join(
                f"'${{{name}}}'"
                for name in missing
            )
        )

    def replace(
        match: re.Match[str],
    ) -> str:
        name = match.group(1)
        value = context[name]

        if value is None:
            raise ValueError(
                f"Template variable '${{{name}}}' "
                "resolved to None."
            )

        return str(value)

    rendered = PLACEHOLDER_PATTERN.sub(
        replace,
        template,
    )

    unresolved = sorted(
        set(
            PLACEHOLDER_PATTERN.findall(
                rendered
            )
        )
    )

    if unresolved:
        raise ValueError(
            "Unresolved template variable(s): "
            + ", ".join(
                f"'${{{name}}}'"
                for name in unresolved
            )
        )

    return rendered


# ----------------------------------------------------------------------
# Template loading
# ----------------------------------------------------------------------


def load_template(
    relative_path: str,
) -> str:
    path = TEMPLATES_DIR / relative_path

    if not path.exists():
        raise FileNotFoundError(
            f"Template does not exist: {path}"
        )

    return path.read_text(
        encoding="utf-8"
    )


# ----------------------------------------------------------------------
# Context
# ----------------------------------------------------------------------


def build_context(
    config: dict[str, Any],
) -> dict[str, Any]:
    entity = config["entity"]

    entity_name = entity["name"]

    entity_name_lower = camel_case(
        entity_name
    )

    fields = entity["fields"]

    foreign_key_context = (
        build_foreign_key_context(
            config.get("relations"),
            current_module=config["module"],
        )
    )

    table_name = entity["table"]

    entity_kebab = kebab_case(
        entity_name
    )

    module_name = config["module"]

    context = {
        "EntityName": entity_name,
        "entityName": entity_name_lower,
        "entityKebab": entity_kebab,

        "moduleName": module_name,
        "tableName": table_name,
        "routeName": module_name,

        "entityImports": (
            "import { randomUUID } "
            "from 'node:crypto';"
        ),

        "entityProps": build_entity_props(
            fields
        ),

        "createEntityParameters":
            build_create_entity_parameters(
                fields
            ),

        "createEntityFields":
            build_create_entity_fields(
                fields
            ),

        "updateMethods":
            build_update_methods(
                fields
            ),

        "getters":
            build_getters(
                fields
            ),

        "createCommandParameters":
            build_create_command_parameters(
                fields
            ),

        "createHandlerFields":
            build_create_handler_fields(
                fields
            ),

        "createHandlerTestArguments":
            build_create_handler_test_arguments(
                fields
            ),

        "updateCommandParameters":
            build_update_command_parameters(
                fields
            ),

        "updateDomainOperation":
            build_update_domain_operation(
                fields,
                entity_name_lower,
            ),

        "persistenceToDomainFields":
            build_persistence_to_domain_fields(
                fields
            ),

        "domainToPersistenceFields":
            build_domain_to_persistence_fields(
                fields,
                entity_name_lower,
            ),

        "ormColumns":
            build_orm_columns(
                fields,
                unique_fields=(
                    foreign_key_context[
                        "uniqueFields"
                    ]
                ),
            ),

        "createValidatorImports":
            build_validator_imports(
                fields,
                required=True,
            ),

        "updateValidatorImports":
            build_validator_imports(
                fields,
                required=False,
            ),

        "createDtoFields":
            build_create_dto_fields(
                fields
            ),

        "updateDtoFields":
            build_update_dto_fields(
                fields
            ),

        "createControllerArguments":
            build_create_controller_arguments(
                fields
            ),

        "updateControllerArguments":
            build_update_controller_arguments(
                fields
            ),

        "typeormImports":
            build_typeorm_imports(
                foreign_key_context[
                    "relationTypeOrmImports"
                ]
            ),
    }

    context.update(
        foreign_key_context
    )

    return context


# ----------------------------------------------------------------------
# Output mapping
# ----------------------------------------------------------------------


def build_output_mapping(
    entity_name: str,
    module_name: str,
) -> dict[str, str]:
    entity_kebab = kebab_case(
        entity_name
    )

    return {
        # Domain
        "domain/entities/entity.entity.ts.tpl":
            f"domain/entities/"
            f"{entity_kebab}.entity.ts",

        "domain/repositories/entity.repository.ts.tpl":
            f"domain/repositories/"
            f"{entity_kebab}.repository.ts",

        "domain/exceptions/entity-not-found.exception.ts.tpl":
            f"domain/exceptions/"
            f"{entity_kebab}-not-found.exception.ts",

        # Commands
        "application/commands/create-entity/create-entity.command.ts.tpl":
            f"application/commands/"
            f"create-{entity_kebab}/"
            f"create-{entity_kebab}.command.ts",

        "application/commands/create-entity/create-entity.handler.ts.tpl":
            f"application/commands/"
            f"create-{entity_kebab}/"
            f"create-{entity_kebab}.handler.ts",

        "application/commands/create-entity/create-entity.handler.spec.ts.tpl":
            f"application/commands/"
            f"create-{entity_kebab}/"
            f"create-{entity_kebab}.handler.spec.ts",

        "application/commands/update-entity/update-entity.command.ts.tpl":
            f"application/commands/"
            f"update-{entity_kebab}/"
            f"update-{entity_kebab}.command.ts",

        "application/commands/update-entity/update-entity.handler.ts.tpl":
            f"application/commands/"
            f"update-{entity_kebab}/"
            f"update-{entity_kebab}.handler.ts",

        "application/commands/delete-entity/delete-entity.command.ts.tpl":
            f"application/commands/"
            f"delete-{entity_kebab}/"
            f"delete-{entity_kebab}.command.ts",

        "application/commands/delete-entity/delete-entity.handler.ts.tpl":
            f"application/commands/"
            f"delete-{entity_kebab}/"
            f"delete-{entity_kebab}.handler.ts",

        # Queries
        "application/queries/get-entity/get-entity.query.ts.tpl":
            f"application/queries/"
            f"get-{entity_kebab}/"
            f"get-{entity_kebab}.query.ts",

        "application/queries/get-entity/get-entity.handler.ts.tpl":
            f"application/queries/"
            f"get-{entity_kebab}/"
            f"get-{entity_kebab}.handler.ts",

        "application/queries/list-entity/list-entity.query.ts.tpl":
            f"application/queries/"
            f"list-{entity_kebab}/"
            f"list-{entity_kebab}.query.ts",

        "application/queries/list-entity/list-entity.handler.ts.tpl":
            f"application/queries/"
            f"list-{entity_kebab}/"
            f"list-{entity_kebab}.handler.ts",

        # Persistence
        "infrastructure/persistence/mappers/entity.persistence-mapper.ts.tpl":
            f"infrastructure/persistence/"
            f"mappers/{entity_kebab}.persistence-mapper.ts",

        "infrastructure/persistence/repositories/typeorm-entity.repository.ts.tpl":
            f"infrastructure/persistence/"
            f"repositories/"
            f"typeorm-{entity_kebab}.repository.ts",

        "infrastructure/persistence/typeorm/entity.orm-entity.ts.tpl":
            f"infrastructure/persistence/"
            f"typeorm/"
            f"{entity_kebab}.orm-entity.ts",

        # Presentation
        "presentation/controllers/entity.controller.ts.tpl":
            f"presentation/controllers/"
            f"{entity_kebab}.controller.ts",

        "presentation/dto/create-entity.dto.ts.tpl":
            f"presentation/dto/"
            f"create-{entity_kebab}.dto.ts",

        "presentation/dto/update-entity.dto.ts.tpl":
            f"presentation/dto/"
            f"update-{entity_kebab}.dto.ts",

        "presentation/filters/entity-exception.filter.ts.tpl":
            f"presentation/filters/"
            f"{entity_kebab}-exception.filter.ts",

        # Module
        "module.ts.tpl":
            f"{module_name}.module.ts",
    }


# ----------------------------------------------------------------------
# Directories
# ----------------------------------------------------------------------


def ensure_directory(
    directory: Path,
) -> None:
    if directory.exists():
        print(
            f"[skipped] directory: {directory}"
        )
        return

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(
        f"[created] directory: {directory}"
    )


def create_directories(
    module_root: Path,
) -> None:
    directories = [
        "application/commands",
        "application/dto",
        "application/handlers",
        "application/queries",

        "domain/entities",
        "domain/events",
        "domain/exceptions",
        "domain/repositories",
        "domain/services",
        "domain/value-objects",

        "infrastructure/persistence/mappers",
        "infrastructure/persistence/repositories",
        "infrastructure/persistence/typeorm",
        "infrastructure/security",

        "presentation/controllers",
        "presentation/dto",
        "presentation/filters",
        "presentation/guards",
        "presentation/serializers",
    ]

    for relative_path in directories:
        ensure_directory(
            module_root / relative_path
        )


# ----------------------------------------------------------------------
# Generation
# ----------------------------------------------------------------------


def generate_module(
    config: dict[str, Any],
    *,
    dry_run: bool = False,
) -> None:
    validate_config(config)

    entity = config["entity"]

    entity_name = entity["name"]
    module_name = config["module"]

    context = build_context(
        config
    )

    output_mapping = build_output_mapping(
        entity_name,
        module_name,
    )

    module_root = (
        MODULES_DIR / module_name
    )

    if dry_run:
        print(
            f"[dry-run] module: {module_root}"
        )
    else:
        create_directories(
            module_root
        )

    for template_path, output_path in (
        output_mapping.items()
    ):
        template = load_template(
            template_path
        )

        rendered = render_template(
            template,
            context,
        )

        destination = (
            module_root / output_path
        )

        if dry_run:
            print(
                f"[dry-run] {destination}"
            )
            continue

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if destination.exists():
            print(
                f"[skipped] file: {destination}"
            )
            continue

        destination.write_text(
            rendered,
            encoding="utf-8",
        )

        print(
            f"created: {destination}"
        )


# ----------------------------------------------------------------------
# YAML loading
# ----------------------------------------------------------------------


def load_config(
    config_path: Path,
) -> dict[str, Any]:
    if not config_path.exists():
        raise FileNotFoundError(
            "Configuration file does not exist: "
            f"{config_path}"
        )

    with config_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        config = yaml.safe_load(file)

    if config is None:
        raise ValueError(
            "Configuration file is empty."
        )

    return config


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate an AtlasCRM module "
            "from a YAML definition."
        )
    )

    parser.add_argument(
        "config",
        type=Path,
        help="Path to the module YAML file.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Validate and render the module "
            "without writing files."
        ),
    )

    args = parser.parse_args()

    try:
        config = load_config(
            args.config
        )

        generate_module(
            config,
            dry_run=args.dry_run,
        )

    except Exception as exc:
        print(
            f"ERROR: {exc}"
        )

        raise SystemExit(1)


if __name__ == "__main__":
    main()