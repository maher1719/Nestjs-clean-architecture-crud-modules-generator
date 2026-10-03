CREATE_COMMAND_TEMPLATE = """\
export class Create${EntityName}Command {
  constructor(${createCommandParameters}) {}
}
"""


CREATE_HANDLER_TEMPLATE = """\
import { Injectable } from '@nestjs/common';

import { ${EntityName} } from '../../../domain/entities/${entityKebab}.entity';
import { ${EntityName}Repository } from '../../../domain/repositories/${entityKebab}.repository';

import { Create${EntityName}Command } from './create-${entityKebab}.command';

@Injectable()
export class Create${EntityName}Handler {
  constructor(
    private readonly repository: ${EntityName}Repository,
  ) {}

  async execute(
    command: Create${EntityName}Command,
  ): Promise<${EntityName}> {
    const entity = ${EntityName}.create(${createHandlerArguments});

    return this.repository.save(entity);
  }
}
"""


UPDATE_COMMAND_TEMPLATE = """\
export class Update${EntityName}Command {
  constructor(
    public readonly id: string,
${updateCommandParameters}
  ) {}
}
"""


UPDATE_HANDLER_TEMPLATE = """\
import { Injectable, NotFoundException } from '@nestjs/common';

import { ${EntityName} } from '../../../domain/entities/${entityKebab}.entity';
import { ${EntityName}Repository } from '../../../domain/repositories/${entityKebab}.repository';

import { Update${EntityName}Command } from './update-${entityKebab}.command';

@Injectable()
export class Update${EntityName}Handler {
  constructor(
    private readonly repository: ${EntityName}Repository,
  ) {}

  async execute(
    command: Update${EntityName}Command,
  ): Promise<${EntityName}> {
    const entity = await this.repository.findById(command.id);

    if (!entity) {
      throw new NotFoundException('${EntityName} not found');
    }

${updateHandlerAssignments}

    return this.repository.save(entity);
  }
}
"""


DELETE_COMMAND_TEMPLATE = """\
export class Delete${EntityName}Command {
  constructor(
    public readonly id: string,
  ) {}
}
"""


DELETE_HANDLER_TEMPLATE = """\
import { Injectable } from '@nestjs/common';

import { ${EntityName}Repository } from '../../../domain/repositories/${entityKebab}.repository';

import { Delete${EntityName}Command } from './delete-${entityKebab}.command';

@Injectable()
export class Delete${EntityName}Handler {
  constructor(
    private readonly repository: ${EntityName}Repository,
  ) {}

  async execute(
    command: Delete${EntityName}Command,
  ): Promise<void> {
    await this.repository.deleteById(command.id);
  }
}
"""


GET_QUERY_TEMPLATE = """\
export class Get${EntityName}Query {
  constructor(
    public readonly id: string,
  ) {}
}
"""


GET_HANDLER_TEMPLATE = """\
import { Injectable, NotFoundException } from '@nestjs/common';

import { ${EntityName} } from '../../../domain/entities/${entityKebab}.entity';
import { ${EntityName}Repository } from '../../../domain/repositories/${entityKebab}.repository';

import { Get${EntityName}Query } from './get-${entityKebab}.query';

@Injectable()
export class Get${EntityName}Handler {
  constructor(
    private readonly repository: ${EntityName}Repository,
  ) {}

  async execute(
    query: Get${EntityName}Query,
  ): Promise<${EntityName}> {
    const entity = await this.repository.findById(query.id);

    if (!entity) {
      throw new NotFoundException('${EntityName} not found');
    }

    return entity;
  }
}
"""


LIST_QUERY_TEMPLATE = """\
export class List${EntityName}Query {}
"""


LIST_HANDLER_TEMPLATE = """\
import { Injectable } from '@nestjs/common';

import { ${EntityName} } from '../../../domain/entities/${entityKebab}.entity';
import { ${EntityName}Repository } from '../../../domain/repositories/${entityKebab}.repository';

import { List${EntityName}Query } from './list-${entityKebab}.query';

@Injectable()
export class List${EntityName}Handler {
  constructor(
    private readonly repository: ${EntityName}Repository,
  ) {}

  async execute(
    query: List${EntityName}Query,
  ): Promise<${EntityName}[]> {
    return this.repository.findAll();
  }
}
"""


APPLICATION_TEMPLATES = {
    "application/commands/create-entity/create-entity.command.ts.tpl": CREATE_COMMAND_TEMPLATE,
    "application/commands/create-entity/create-entity.handler.ts.tpl": CREATE_HANDLER_TEMPLATE,
    "application/commands/update-entity/update-entity.command.ts.tpl": UPDATE_COMMAND_TEMPLATE,
    "application/commands/update-entity/update-entity.handler.ts.tpl": UPDATE_HANDLER_TEMPLATE,
    "application/commands/delete-entity/delete-entity.command.ts.tpl": DELETE_COMMAND_TEMPLATE,
    "application/commands/delete-entity/delete-entity.handler.ts.tpl": DELETE_HANDLER_TEMPLATE,
    "application/queries/get-entity/get-entity.query.ts.tpl": GET_QUERY_TEMPLATE,
    "application/queries/get-entity/get-entity.handler.ts.tpl": GET_HANDLER_TEMPLATE,
    "application/queries/list-entity/list-entity.query.ts.tpl": LIST_QUERY_TEMPLATE,
    "application/queries/list-entity/list-entity.handler.ts.tpl": LIST_HANDLER_TEMPLATE,
}