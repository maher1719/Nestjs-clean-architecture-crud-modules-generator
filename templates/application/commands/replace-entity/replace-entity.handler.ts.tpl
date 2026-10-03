import { Injectable, NotFoundException } from '@nestjs/common';

import { ${EntityName} } from '../../../domain/entities/${entityKebab}.entity';
import { ${EntityName}Repository } from '../../../domain/repositories/${entityKebab}.repository';

import { Replace${EntityName}Command } from './replace-${entityKebab}.command';

@Injectable()
export class Replace${EntityName}Handler {
  constructor(
    private readonly repository: ${EntityName}Repository,
  ) {}

  async execute(
    command: Replace${EntityName}Command,
  ): Promise<${EntityName}> {
    const entity = await this.repository.findById(command.id);

    if (!entity) {
      throw new NotFoundException('${EntityName} not found');
    }

${updateHandlerAssignments}

    return this.repository.save(entity);
  }
}
