import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';

import { ${EntityName}OrmEntity } from './infrastructure/persistence/typeorm/${entityKebab}.orm-entity';
import { TypeOrm${EntityName}Repository } from './infrastructure/persistence/repositories/typeorm-${entityKebab}.repository';
import { ${EntityName}Repository } from './domain/repositories/${entityKebab}.repository';

import { Create${EntityName}Handler } from './application/commands/create-${entityKebab}/create-${entityKebab}.handler';
import { Update${EntityName}Handler } from './application/commands/update-${entityKebab}/update-${entityKebab}.handler';
import { Delete${EntityName}Handler } from './application/commands/delete-${entityKebab}/delete-${entityKebab}.handler';

import { Get${EntityName}Handler } from './application/queries/get-${entityKebab}/get-${entityKebab}.handler';
import { List${EntityName}Handler } from './application/queries/list-${entityKebab}/list-${entityKebab}.handler';

import { ${EntityName}Controller } from './presentation/controllers/${entityKebab}.controller';

@Module({
  imports: [
    TypeOrmModule.forFeature([
      ${EntityName}OrmEntity,
    ]),
  ],
  controllers: [
    ${EntityName}Controller,
  ],
  providers: [
    Create${EntityName}Handler,
    Update${EntityName}Handler,
    Delete${EntityName}Handler,
    Get${EntityName}Handler,
    List${EntityName}Handler,
    TypeOrm${EntityName}Repository,
    {
      provide: ${EntityName}Repository,
      useExisting: TypeOrm${EntityName}Repository,
    },
  ],
  exports: [
    ${EntityName}Repository,
  ],
})
export class ${EntityName}Module {}
