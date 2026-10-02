import { Inject } from '@nestjs/common';
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
