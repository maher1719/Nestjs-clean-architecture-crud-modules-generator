import { Inject, Injectable } from '@nestjs/common';
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
