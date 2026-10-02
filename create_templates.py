from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"


TEMPLATES = {
    # ------------------------------------------------------------------
    # Domain
    # ------------------------------------------------------------------

    "domain/entities/entity.entity.ts.tpl": """${entityImports}

export interface ${EntityName}Props {
  id: string;
${entityProps}
  createdAt: Date;
  updatedAt: Date;
}

export class ${EntityName} {
  private constructor(
    private props: ${EntityName}Props,
  ) {}

  static create(
${createEntityParameters}
  ): ${EntityName} {
    const now = new Date();

    return new ${EntityName}({
      id: randomUUID(),
${createEntityFields}
      createdAt: now,
      updatedAt: now,
    });
  }

  static reconstitute(
    props: ${EntityName}Props,
  ): ${EntityName} {
    return new ${EntityName}(props);
  }

${updateMethods}

${getters}
}
""",

    "domain/repositories/entity.repository.ts.tpl": """import { ${EntityName} } from '../entities/${entityKebab}.entity';

export abstract class ${EntityName}Repository {
  abstract findAll(): Promise<${EntityName}[]>;
  abstract findById(id: string): Promise<${EntityName} | null>;
  abstract save(${entityName}: ${EntityName}): Promise<void>;
  abstract delete(${entityName}: ${EntityName}): Promise<void>;
}
""",

    "domain/exceptions/entity-not-found.exception.ts.tpl": """export class ${EntityName}NotFoundException extends Error {
  constructor() {
    super('${EntityName} not found.');
    this.name = '${EntityName}NotFoundException';
  }
}
""",

    # ------------------------------------------------------------------
    # Application / Commands
    # ------------------------------------------------------------------

    "application/commands/create-entity/create-entity.command.ts.tpl": """export class Create${EntityName}Command {
  constructor(
${createCommandParameters}
  ) {}
}
""",

    "application/commands/create-entity/create-entity.handler.ts.tpl": """import { Inject } from '@nestjs/common';
import { Create${EntityName}Command } from './create-${entityKebab}.command';
import { ${EntityName} } from '../../../domain/entities/${entityKebab}.entity';
import { ${EntityName}Repository } from '../../../domain/repositories/${entityKebab}.repository';

export class Create${EntityName}Handler {
  constructor(
    @Inject(${EntityName}Repository)
    private readonly ${entityName}Repository: ${EntityName}Repository,
  ) {}

  async execute(
    command: Create${EntityName}Command,
  ): Promise<${EntityName}> {
    const ${entityName} = ${EntityName}.create(
${createHandlerFields}
    );

    await this.${entityName}Repository.save(${entityName});

    return ${entityName};
  }
}
""",

    "application/commands/create-entity/create-entity.handler.spec.ts.tpl": """import { Create${EntityName}Command } from './create-${entityKebab}.command';
import { Create${EntityName}Handler } from './create-${entityKebab}.handler';
import { ${EntityName}Repository } from '../../../domain/repositories/${entityKebab}.repository';

describe('Create${EntityName}Handler', () => {
  let handler: Create${EntityName}Handler;
  let repository: jest.Mocked<${EntityName}Repository>;

  beforeEach(() => {
    repository = {
      findAll: jest.fn(),
      findById: jest.fn(),
      save: jest.fn(),
      delete: jest.fn(),
    };

    handler = new Create${EntityName}Handler(repository);
  });

  it('creates an ${entityName}', async () => {
    const command = new Create${EntityName}Command(
${createHandlerTestArguments}
    );

    const result = await handler.execute(command);

    expect(result).toBeInstanceOf(${EntityName});
    expect(repository.save).toHaveBeenCalledWith(result);
  });
});
""",

    "application/commands/update-entity/update-entity.command.ts.tpl": """export class Update${EntityName}Command {
  constructor(
    public readonly id: string,
${updateCommandParameters}
  ) {}
}
""",

    "application/commands/update-entity/update-entity.handler.ts.tpl": """import { Inject } from '@nestjs/common';
import { Update${EntityName}Command } from './update-${entityKebab}.command';
import { ${EntityName} } from '../../../domain/entities/${entityKebab}.entity';
import { ${EntityName}Repository } from '../../../domain/repositories/${entityKebab}.repository';
import { ${EntityName}NotFoundException } from '../../../domain/exceptions/${entityKebab}-not-found.exception';

export class Update${EntityName}Handler {
  constructor(
    @Inject(${EntityName}Repository)
    private readonly ${entityName}Repository: ${EntityName}Repository,
  ) {}

  async execute(
    command: Update${EntityName}Command,
  ): Promise<${EntityName}> {
    const ${entityName} = await this.${entityName}Repository.findById(
      command.id,
    );

    if (!${entityName}) {
      throw new ${EntityName}NotFoundException();
    }

${updateDomainOperation}

    await this.${entityName}Repository.save(${entityName});

    return ${entityName};
  }
}
""",

    "application/commands/delete-entity/delete-entity.command.ts.tpl": """export class Delete${EntityName}Command {
  constructor(
    public readonly id: string,
  ) {}
}
""",

    "application/commands/delete-entity/delete-entity.handler.ts.tpl": """import { Inject } from '@nestjs/common';
import { Delete${EntityName}Command } from './delete-${entityKebab}.command';
import { ${EntityName}Repository } from '../../../domain/repositories/${entityKebab}.repository';
import { ${EntityName}NotFoundException } from '../../../domain/exceptions/${entityKebab}-not-found.exception';

export class Delete${EntityName}Handler {
  constructor(
    @Inject(${EntityName}Repository)
    private readonly ${entityName}Repository: ${EntityName}Repository,
  ) {}

  async execute(
    command: Delete${EntityName}Command,
  ): Promise<void> {
    const ${entityName} = await this.${entityName}Repository.findById(
      command.id,
    );

    if (!${entityName}) {
      throw new ${EntityName}NotFoundException();
    }

    await this.${entityName}Repository.delete(${entityName});
  }
}
""",

    # ------------------------------------------------------------------
    # Application / Queries
    # ------------------------------------------------------------------

    "application/queries/get-entity/get-entity.query.ts.tpl": """export class Get${EntityName}Query {
  constructor(
    public readonly id: string,
  ) {}
}
""",

    "application/queries/get-entity/get-entity.handler.ts.tpl": """import { Inject, Injectable } from '@nestjs/common';
import { Get${EntityName}Query } from './get-${entityKebab}.query';
import { ${EntityName} } from '../../../domain/entities/${entityKebab}.entity';
import { ${EntityName}Repository } from '../../../domain/repositories/${entityKebab}.repository';
import { ${EntityName}NotFoundException } from '../../../domain/exceptions/${entityKebab}-not-found.exception';

@Injectable()
export class Get${EntityName}Handler {
  constructor(
    @Inject(${EntityName}Repository)
    private readonly ${entityName}Repository: ${EntityName}Repository,
  ) {}

  async execute(
    query: Get${EntityName}Query,
  ): Promise<${EntityName}> {
    const ${entityName} = await this.${entityName}Repository.findById(
      query.id,
    );

    if (!${entityName}) {
      throw new ${EntityName}NotFoundException();
    }

    return ${entityName};
  }
}
""",

    "application/queries/list-entity/list-entity.query.ts.tpl": """export class List${EntityName}Query {}
""",

    "application/queries/list-entity/list-entity.handler.ts.tpl": """import { Inject, Injectable } from '@nestjs/common';
import { List${EntityName}Query } from './list-${entityKebab}.query';
import { ${EntityName} } from '../../../domain/entities/${entityKebab}.entity';
import { ${EntityName}Repository } from '../../../domain/repositories/${entityKebab}.repository';

@Injectable()
export class List${EntityName}Handler {
  constructor(
    @Inject(${EntityName}Repository)
    private readonly ${entityName}Repository: ${EntityName}Repository,
  ) {}

  async execute(
    _query: List${EntityName}Query,
  ): Promise<${EntityName}[]> {
    return this.${entityName}Repository.findAll();
  }
}
""",

    # ------------------------------------------------------------------
    # Infrastructure / Persistence
    # ------------------------------------------------------------------

    "infrastructure/persistence/mappers/entity.persistence-mapper.ts.tpl": """import { ${EntityName} } from '../../../domain/entities/${entityKebab}.entity';
import { ${EntityName}OrmEntity } from '../typeorm/${entityKebab}.orm-entity';

export class ${EntityName}PersistenceMapper {
  static toDomain(
    entity: ${EntityName}OrmEntity,
  ): ${EntityName} {
    return ${EntityName}.reconstitute({
${persistenceToDomainFields}
    });
  }

  static toPersistence(
    ${entityName}: ${EntityName},
  ): ${EntityName}OrmEntity {
    const entity = new ${EntityName}OrmEntity();

${domainToPersistenceFields}

    return entity;
  }
}
""",

    "infrastructure/persistence/repositories/typeorm-entity.repository.ts.tpl": """import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';

import { ${EntityName} } from '../../../domain/entities/${entityKebab}.entity';
import { ${EntityName}Repository } from '../../../domain/repositories/${entityKebab}.repository';
import { ${EntityName}PersistenceMapper } from '../mappers/${entityKebab}.persistence-mapper';
import { ${EntityName}OrmEntity } from '../typeorm/${entityKebab}.orm-entity';

@Injectable()
export class TypeOrm${EntityName}Repository
  implements ${EntityName}Repository
{
  constructor(
    @InjectRepository(${EntityName}OrmEntity)
    private readonly repository: Repository<${EntityName}OrmEntity>,
  ) {}

  async findAll(): Promise<${EntityName}[]> {
    const entities = await this.repository.find();

    return entities.map(
      ${entityName} =>
        ${EntityName}PersistenceMapper.toDomain(${entityName}),
    );
  }

  async findById(id: string): Promise<${EntityName} | null> {
    const entity = await this.repository.findOne({
      where: { id },
    });

    if (!entity) {
      return null;
    }

    return ${EntityName}PersistenceMapper.toDomain(entity);
  }

  async save(
    ${entityName}: ${EntityName},
  ): Promise<void> {
    const entity =
      ${EntityName}PersistenceMapper.toPersistence(${entityName});

    await this.repository.save(entity);
  }

  async delete(
    ${entityName}: ${EntityName},
  ): Promise<void> {
    await this.repository.delete(${entityName}.getId());
  }
}
""",

    "infrastructure/persistence/typeorm/entity.orm-entity.ts.tpl": """${typeormImports}

${relationImports}

@Entity('${tableName}')
export class ${EntityName}OrmEntity {
  @PrimaryColumn('uuid')
  id!: string;

${ormColumns}

${ormRelations}

  @CreateDateColumn({ type: 'timestamptz' })
  createdAt!: Date;

  @UpdateDateColumn({ type: 'timestamptz' })
  updatedAt!: Date;
}
""",

    # ------------------------------------------------------------------
    # Presentation
    # ------------------------------------------------------------------

    "presentation/controllers/entity.controller.ts.tpl": """import {
  Body,
  Controller,
  Delete,
  Get,
  Param,
  Post,
  Put,
  Patch,
} from '@nestjs/common';

import { ApiTags } from '@nestjs/swagger';

import { Create${EntityName}Command } from '../../application/commands/create-${entityKebab}/create-${entityKebab}.command';
import { Create${EntityName}Handler } from '../../application/commands/create-${entityKebab}/create-${entityKebab}.handler';

import { Update${EntityName}Command } from '../../application/commands/update-${entityKebab}/update-${entityKebab}.command';
import { Update${EntityName}Handler } from '../../application/commands/update-${entityKebab}/update-${entityKebab}.handler';

import { Delete${EntityName}Command } from '../../application/commands/delete-${entityKebab}/delete-${entityKebab}.command';
import { Delete${EntityName}Handler } from '../../application/commands/delete-${entityKebab}/delete-${entityKebab}.handler';

import { Get${EntityName}Query } from '../../application/queries/get-${entityKebab}/get-${entityKebab}.query';
import { Get${EntityName}Handler } from '../../application/queries/get-${entityKebab}/get-${entityKebab}.handler';

import { List${EntityName}Query } from '../../application/queries/list-${entityKebab}/list-${entityKebab}.query';
import { List${EntityName}Handler } from '../../application/queries/list-${entityKebab}/list-${entityKebab}.handler';

import { Create${EntityName}Dto } from '../dto/create-${entityKebab}.dto';
import { Update${EntityName}Dto } from '../dto/update-${entityKebab}.dto';

@ApiTags('${moduleName}')
@Controller('${routeName}')
export class ${EntityName}Controller {
  constructor(
    private readonly createHandler: Create${EntityName}Handler,
    private readonly updateHandler: Update${EntityName}Handler,
    private readonly deleteHandler: Delete${EntityName}Handler,
    private readonly getHandler: Get${EntityName}Handler,
    private readonly listHandler: List${EntityName}Handler,
  ) {}

  @Post()
  async create(
    @Body() dto: Create${EntityName}Dto,
  ) {
    const command = new Create${EntityName}Command(
${createControllerArguments}
    );

    return this.createHandler.execute(command);
  }

  @Get()
  async findAll() {
    return this.listHandler.execute(
      new List${EntityName}Query(),
    );
  }

  @Get(':id')
  async findOne(
    @Param('id') id: string,
  ) {
    return this.getHandler.execute(
      new Get${EntityName}Query(id),
    );
  }

/*
  @Put(':id')
  async update(
    @Param('id') id: string,
    @Body() dto: Update${EntityName}Dto,
  ) {
    const command = new Update${EntityName}Command(
      id,
${updateControllerArguments}
    );

    return this.updateHandler.execute(command);
  }*/


  @Patch(':id')
  async update(
    @Param('id') id: string,
    @Body() dto: Update${EntityName}Dto,
  ) {
    const command = new Update${EntityName}Command(
      id,
${updateControllerArguments}
    );

    return this.updateHandler.execute(command);
  }

  @Delete(':id')
  async remove(
    @Param('id') id: string,
  ): Promise<void> {
    return this.deleteHandler.execute(
      new Delete${EntityName}Command(id),
    );
  }
}
""",

    "presentation/dto/create-entity.dto.ts.tpl": """import { ApiProperty } from '@nestjs/swagger';

import {
  ${createValidatorImports},
} from 'class-validator';

export class Create${EntityName}Dto {
${createDtoFields}
}
""",

    "presentation/dto/update-entity.dto.ts.tpl": """import { ApiPropertyOptional } from '@nestjs/swagger';

import {
  ${updateValidatorImports},
} from 'class-validator';

export class Update${EntityName}Dto {
${updateDtoFields}
}
""",

    "presentation/filters/entity-exception.filter.ts.tpl": """import {
  ArgumentsHost,
  Catch,
  ExceptionFilter,
  HttpStatus,
} from '@nestjs/common';

import { ${EntityName}NotFoundException } from '../../domain/exceptions/${entityKebab}-not-found.exception';

@Catch(${EntityName}NotFoundException)
export class ${EntityName}ExceptionFilter
  implements ExceptionFilter
{
  catch(
    exception: ${EntityName}NotFoundException,
    host: ArgumentsHost,
  ): void {
    const response = host.switchToHttp().getResponse();

    response.status(HttpStatus.NOT_FOUND).json({
      statusCode: HttpStatus.NOT_FOUND,
      message: exception.message,
    });
  }
}
""",

    # ------------------------------------------------------------------
    # Module
    # ------------------------------------------------------------------

    "module.ts.tpl": """import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';

import { ${EntityName}OrmEntity } from './infrastructure/persistence/typeorm/${entityKebab}.orm-entity';
import { TypeOrm${EntityName}Repository } from './infrastructure/persistence/repositories/typeorm-${entityKebab}.repository';
import { ${EntityName}Repository } from './domain/repositories/${entityKebab}.repository';

import { Create${EntityName}Handler } from './application/commands/create-${entityKebab}/create-${entityKebab}.handler';
import { Update${EntityName}Handler } from './application/commands/update-${entityKebab}/update-${entityKebab}.handler';
import { Delete${EntityName}Handler } from './application/commands/delete-${entityKebab}/delete-${entityKebab}.handler';

import { Get${EntityName}Handler } from './application/queries/get-${entityKebab}/get-${entityKebab}.handler';
import { List${EntityName}Handler } from './application/queries/list-${entityKebab}/list-${entityKebab}.handler';

import { ${EntityName}Controller } from './presentation/controllers/${entityKebab}.controller';

@Module({
  imports: [
    TypeOrmModule.forFeature([
      ${EntityName}OrmEntity,
    ]),
  ],
  controllers: [
    ${EntityName}Controller,
  ],
  providers: [
    Create${EntityName}Handler,
    Update${EntityName}Handler,
    Delete${EntityName}Handler,
    Get${EntityName}Handler,
    List${EntityName}Handler,
    TypeOrm${EntityName}Repository,
    {
      provide: ${EntityName}Repository,
      useExisting: TypeOrm${EntityName}Repository,
    },
  ],
  exports: [
    ${EntityName}Repository,
  ],
})
export class ${EntityName}Module {}
""",
}


def create_templates() -> None:
    TEMPLATES_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    for relative_path, content in TEMPLATES.items():
        template_path = TEMPLATES_DIR / relative_path

        template_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        template_path.write_text(
            content,
            encoding="utf-8",
        )

        print(f"created template: {template_path}")


if __name__ == "__main__":
    create_templates()
