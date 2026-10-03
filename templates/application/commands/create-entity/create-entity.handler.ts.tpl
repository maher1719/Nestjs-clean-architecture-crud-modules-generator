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
