from typing import Dict

from .naming import kebab_case


def build_output_mapping(
    entity_name: str,
    module_name: str,
) -> Dict[str, str]:
    entity_kebab = kebab_case(entity_name)

    return {
        # Domain
        "domain/entities/entity.entity.ts.tpl": (
            f"domain/entities/{entity_kebab}.entity.ts"
        ),
        "domain/repositories/entity.repository.ts.tpl": (
            f"domain/repositories/{entity_kebab}.repository.ts"
        ),

        # Application commands
        "application/commands/create-entity/create-entity.command.ts.tpl": (
            f"application/commands/create-{entity_kebab}/"
            f"create-{entity_kebab}.command.ts"
        ),
        "application/commands/create-entity/create-entity.handler.ts.tpl": (
            f"application/commands/create-{entity_kebab}/"
            f"create-{entity_kebab}.handler.ts"
        ),
        "application/commands/update-entity/update-entity.command.ts.tpl": (
            f"application/commands/update-{entity_kebab}/"
            f"update-{entity_kebab}.command.ts"
        ),
        "application/commands/update-entity/update-entity.handler.ts.tpl": (
            f"application/commands/update-{entity_kebab}/"
            f"update-{entity_kebab}.handler.ts"
        ),
        "application/commands/delete-entity/delete-entity.command.ts.tpl": (
            f"application/commands/delete-{entity_kebab}/"
            f"delete-{entity_kebab}.command.ts"
        ),
        "application/commands/delete-entity/delete-entity.handler.ts.tpl": (
            f"application/commands/delete-{entity_kebab}/"
            f"delete-{entity_kebab}.handler.ts"
        ),

        # Application replace commands
        "application/commands/replace-entity/replace-entity.command.ts.tpl": (
            f"application/commands/replace-{entity_kebab}/"
            f"replace-{entity_kebab}.command.ts"
        ),
        "application/commands/replace-entity/replace-entity.handler.ts.tpl": (
            f"application/commands/replace-{entity_kebab}/"
            f"replace-{entity_kebab}.handler.ts"
        ),

        # Presentation replace DTO
        "presentation/dto/replace-entity.dto.ts.tpl": (
            f"presentation/dto/replace-{entity_kebab}.dto.ts"
        ),

        # Application queries
        "application/queries/get-entity/get-entity.query.ts.tpl": (
            f"application/queries/get-{entity_kebab}/"
            f"get-{entity_kebab}.query.ts"
        ),
        "application/queries/get-entity/get-entity.handler.ts.tpl": (
            f"application/queries/get-{entity_kebab}/"
            f"get-{entity_kebab}.handler.ts"
        ),
        "application/queries/list-entity/list-entity.query.ts.tpl": (
            f"application/queries/list-{entity_kebab}/"
            f"list-{entity_kebab}.query.ts"
        ),
        "application/queries/list-entity/list-entity.handler.ts.tpl": (
            f"application/queries/list-{entity_kebab}/"
            f"list-{entity_kebab}.handler.ts"
        ),

        # Infrastructure persistence
        "infrastructure/persistence/typeorm/entity.orm-entity.ts.tpl": (
            f"infrastructure/persistence/typeorm/"
            f"{entity_kebab}.orm-entity.ts"
        ),
        "infrastructure/persistence/mappers/entity.persistence-mapper.ts.tpl": (
            f"infrastructure/persistence/mappers/"
            f"{entity_kebab}.persistence-mapper.ts"
        ),
        "infrastructure/persistence/typeorm/entity.typeorm-repository.ts.tpl": (
            f"infrastructure/persistence/typeorm/"
            f"{entity_kebab}.typeorm-repository.ts"
        ),

        # Presentation
        "presentation/controllers/entity.controller.ts.tpl": (
            f"presentation/controllers/{entity_kebab}.controller.ts"
        ),
        "presentation/dto/create-entity.dto.ts.tpl": (
            f"presentation/dto/create-{entity_kebab}.dto.ts"
        ),
        "presentation/dto/update-entity.dto.ts.tpl": (
            f"presentation/dto/update-{entity_kebab}.dto.ts"
        ),

        # Module
        "module.ts.tpl": (
            f"{module_name}.module.ts"
        ),
    }
