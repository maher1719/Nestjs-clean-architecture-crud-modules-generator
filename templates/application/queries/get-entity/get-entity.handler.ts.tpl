import { Inject, Injectable } from '@nestjs/common';
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
