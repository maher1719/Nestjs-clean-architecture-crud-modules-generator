import { Inject } from '@nestjs/common';
import { Update${EntityName}Command } from './update-${entityKebab}.command';
import { ${EntityName} } from '../../../domain/entities/${entityKebab}.entity';
import { ${EntityName}Repository } from '../../../domain/repositories/${entityKebab}.repository';
import { ${EntityName}NotFoundException } from '../../../domain/exceptions/${entityKebab}-not-found.exception';

export class Update${EntityName}Handler {
  constructor(
    @Inject(${EntityName}Repository)
    private readonly ${entityName}Repository: ${EntityName}Repository,
  ) {}

  async execute(
    command: Update${EntityName}Command,
  ): Promise<${EntityName}> {
    const ${entityName} = await this.${entityName}Repository.findById(
      command.id,
    );

    if (!${entityName}) {
      throw new ${EntityName}NotFoundException();
    }

${updateDomainOperation}

    await this.${entityName}Repository.save(${entityName});

    return ${entityName};
  }
}
