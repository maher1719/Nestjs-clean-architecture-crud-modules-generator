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
