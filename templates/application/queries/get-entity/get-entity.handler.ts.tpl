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
