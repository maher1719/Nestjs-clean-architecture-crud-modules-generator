from typing import List

from ..naming import change_method_name
from .types import Field, ts_type


def build_entity_props(fields: List[Field]) -> str:
    lines = []
    for field in fields:
        name = field["name"]
        lines.append(f"  {name}: {ts_type(field)};")
    return "\n".join(lines)


def build_create_entity_parameters(fields: List[Field]) -> str:
    lines = []
    for field in fields:
        name = field["name"]
        lines.append(f"    {name}: {ts_type(field)},")
    return "\n".join(lines)


def build_create_entity_fields(fields: List[Field]) -> str:
    lines = []
    for field in fields:
        lines.append(f"      {field['name']},")
    return "\n".join(lines)


def build_create_command_parameters(fields: List[Field]) -> str:
    parts = []
    for field in fields:
        name = field["name"]
        parts.append(f"public readonly {name}: {ts_type(field)}")
    return ", ".join(parts)


def build_create_handler_arguments(fields: List[Field]) -> str:
    parts = []
    for field in fields:
        parts.append(f"command.{field['name']}")
    return ", ".join(parts)


def build_create_controller_arguments(fields: List[Field]) -> str:
    lines = []
    for field in fields:
        lines.append(f"      dto.{field['name']},")
    return "\n".join(lines)


def build_update_command_parameters(fields: List[Field]) -> str:
    lines = []
    for field in fields:
        name = field["name"]
        lines.append(f"    public readonly {name}?: {ts_type(field)},")
    return "\n".join(lines)


def build_update_controller_arguments(fields: List[Field]) -> str:
    lines = []
    for field in fields:
        lines.append(f"      dto.{field['name']},")
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

def build_replace_command_parameters(fields: List[Field]) -> str:
    lines = []
    for field in fields:
        name = field["name"]
        field_ts_type = ts_type(field)
        # Replace = all fields REQUIRED (no `?`), one per line
        lines.append(f"    public readonly {name}: {field_ts_type},")
    return "\n".join(lines)


def build_replace_controller_arguments(fields: List[Field]) -> str:
    lines = []
    for field in fields:
        lines.append(f"      dto.{field['name']},")
    return "\n".join(lines)

    
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
