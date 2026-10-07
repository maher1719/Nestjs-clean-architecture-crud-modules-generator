from typing import Dict, List

from .domain import (
    build_create_command_parameters,
    build_create_controller_arguments,
    build_create_entity_fields,
    build_create_entity_parameters,
    build_create_handler_arguments,
    build_entity_props,
    build_getters,
    build_update_command_parameters,
    build_update_controller_arguments,
    build_update_handler_assignments,
    build_update_methods,
    build_replace_command_parameters,
    build_replace_controller_arguments,
)
from .dto import (
    build_create_dto_fields,
    build_update_dto_fields,
    build_replace_dto_fields,
    build_validator_imports,
)
from .mapping import (
    build_domain_to_orm_fields,
    build_orm_to_domain_fields,
)
from .types import Field


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
        "replaceValidatorImports": build_validator_imports(fields, required=True),
        "replaceDtoFields": build_replace_dto_fields(fields),
    }
