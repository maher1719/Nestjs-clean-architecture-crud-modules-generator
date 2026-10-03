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
