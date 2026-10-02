import { Inject } from '@nestjs/common';
import { Delete${EntityName}Command } from './delete-${entityKebab}.command';
import { ${EntityName}Repository } from '../../../domain/repositories/${entityKebab}.repository';
import { ${EntityName}NotFoundException } from '../../../domain/exceptions/${entityKebab}-not-found.exception';

export class Delete${EntityName}Handler {
  constructor(
    @Inject(${EntityName}Repository)
    private readonly ${entityName}Repository: ${EntityName}Repository,
  ) {}

  async execute(
    command: Delete${EntityName}Command,
  ): Promise<void> {
    const ${entityName} = await this.${entityName}Repository.findById(
      command.id,
    );

    if (!${entityName}) {
      throw new ${EntityName}NotFoundException();
    }

    await this.${entityName}Repository.delete(${entityName});
  }
}
