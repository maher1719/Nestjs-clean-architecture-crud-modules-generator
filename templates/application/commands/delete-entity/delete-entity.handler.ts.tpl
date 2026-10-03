import { Injectable } from '@nestjs/common';

import { ${EntityName}Repository } from '../../../domain/repositories/${entityKebab}.repository';

import { Delete${EntityName}Command } from './delete-${entityKebab}.command';

@Injectable()
export class Delete${EntityName}Handler {
  constructor(
    private readonly repository: ${EntityName}Repository,
  ) {}

  async execute(
    command: Delete${EntityName}Command,
  ): Promise<void> {
    await this.repository.deleteById(command.id);
  }
}
