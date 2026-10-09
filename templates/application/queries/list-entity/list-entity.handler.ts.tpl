import { Inject, Injectable } from '@nestjs/common';
import { ${EntityName} } from '../../../domain/entities/${entityKebab}.entity';
import { ${EntityName}Repository } from '../../../domain/repositories/${entityKebab}.repository';
import { List${EntityName}Query } from './list-${entityKebab}.query';
import { Paginated } from '../../../domain/repositories/list-options';




@Injectable()
export class List${EntityName}Handler {
    constructor(
    @Inject(${EntityName}Repository)
    private readonly ${entityName}Repository: ${EntityName}Repository,
  ) {}

  async execute(
    query: List${EntityName}Query,
  ): Promise<Paginated<${EntityName}>> {
    return this.${entityName}Repository.findAll(query.options);
  }
}
