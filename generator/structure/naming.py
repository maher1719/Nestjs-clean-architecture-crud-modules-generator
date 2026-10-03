import re


def kebab_case(value: str) -> str:
    if not value:
        return ""

    value = re.sub(r"(?<!^)(?=[A-Z])", "-", value)
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value)
    value = value.strip("-")

    return value.lower()


def camel_case(value: str) -> str:
    if not value:
        return ""

    return value[:1].lower() + value[1:]


def pascal_case(value: str) -> str:
    if not value:
        return ""

    return value[:1].upper() + value[1:]


def change_method_name(field_name: str) -> str:
    return "change" + pascal_case(field_name)
