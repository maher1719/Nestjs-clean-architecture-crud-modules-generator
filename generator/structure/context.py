from typing import Any, Dict

from .fields import (
    build_field_context,
    build_orm_columns,
    build_typeorm_imports,
    normalize_fields,
    normalize_relations,
)
from .naming import camel_case, kebab_case


def build_context(config: Dict[str, Any]) -> Dict[str, str]:
    entity = config["entity"]
    module_name = config["module"]

    entity_name = entity["name"]
    table_name = entity["table"]

    entity_name_lower = camel_case(entity_name)
    entity_kebab = kebab_case(entity_name)

    fields = normalize_fields(entity.get("fields", []))
    relations = normalize_relations(config.get("relations", []))

    context = {
        "EntityName": entity_name,
        "entityName": entity_name_lower,
        "entityKebab": entity_kebab,
        "moduleName": module_name,
        "tableName": table_name,
        "routeName": module_name,
        "entityImports": "import { randomUUID } from 'node:crypto';",
    }

    context.update(build_field_context(fields))

    context["ormColumns"] = build_orm_columns(
        fields,
        relations,
        module_name,
    )

    context["typeormImports"] = build_typeorm_imports(
        relations,
        module_name,
    )

    context.update(
        build_module_context(
            entity_name=entity_name,
            entity_kebab=entity_kebab,
        )
    )

    return context


def build_module_context(
    entity_name: str,
    entity_kebab: str,
) -> Dict[str, str]:
    controller_import = (
        f"import {{ {entity_name}Controller }} "
        f"from './presentation/controllers/{entity_kebab}.controller';"
    )

    create_handler_import = (
        f"import {{ Create{entity_name}Handler }} "
        f"from './application/commands/create-{entity_kebab}/create-{entity_kebab}.handler';"
    )

    update_handler_import = (
        f"import {{ Update{entity_name}Handler }} "
        f"from './application/commands/update-{entity_kebab}/update-{entity_kebab}.handler';"
    )

    delete_handler_import = (
        f"import {{ Delete{entity_name}Handler }} "
        f"from './application/commands/delete-{entity_kebab}/delete-{entity_kebab}.handler';"
    )

    get_handler_import = (
        f"import {{ Get{entity_name}Handler }} "
        f"from './application/queries/get-{entity_kebab}/get-{entity_kebab}.handler';"
    )

    list_handler_import = (
        f"import {{ List{entity_name}Handler }} "
        f"from './application/queries/list-{entity_kebab}/list-{entity_kebab}.handler';"
    )

    replace_handler_import = (
        f"import {{ Replace{entity_name}Handler }} "
        f"from './application/commands/replace-{entity_kebab}/replace-{entity_kebab}.handler';"
    )

    repository_import = (
        f"import {{ {entity_name}Repository }} "
        f"from './domain/repositories/{entity_kebab}.repository';"
    )

    typeorm_repository_import = (
        f"import {{ TypeOrm{entity_name}Repository }} "
        f"from './infrastructure/persistence/typeorm/{entity_kebab}.typeorm-repository';"
    )
    entity_orm_import = (
        f"import {{ {entity_name}OrmEntity }} "
        f"from './infrastructure/persistence/typeorm/{entity_kebab}.orm-entity';"
    )

    module_imports = [
        controller_import,
        create_handler_import,
        update_handler_import,
        replace_handler_import,
        delete_handler_import,
        get_handler_import,
        list_handler_import,
        repository_import,
        entity_orm_import,
        typeorm_repository_import,
    ]

    module_providers = [
        f"    Create{entity_name}Handler,",
        f"    Update{entity_name}Handler,",
        f"    Replace{entity_name}Handler,",
        f"    Delete{entity_name}Handler,",
        f"    Get{entity_name}Handler,",
        f"    List{entity_name}Handler,",
        "    {",
        f"      provide: {entity_name}Repository,",
        f"      useClass: TypeOrm{entity_name}Repository,",
        "    },",
    ]

    module_exports = [
        f"    {entity_name}Repository,",
    ]

    return {
        "moduleImports": "\n".join(module_imports),
        "moduleControllers": f"{entity_name}Controller",
        "moduleProviders": "\n".join(module_providers),
        "moduleExports": "\n".join(module_exports),
    }
