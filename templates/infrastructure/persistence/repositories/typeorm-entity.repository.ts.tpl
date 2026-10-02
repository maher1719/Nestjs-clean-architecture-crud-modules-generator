import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';

import { ${EntityName} } from '../../../domain/entities/${entityKebab}.entity';
import { ${EntityName}Repository } from '../../../domain/repositories/${entityKebab}.repository';
import { ${EntityName}PersistenceMapper } from '../mappers/${entityKebab}.persistence-mapper';
import { ${EntityName}OrmEntity } from '../typeorm/${entityKebab}.orm-entity';

@Injectable()
export class TypeOrm${EntityName}Repository
  implements ${EntityName}Repository
{
  constructor(
    @InjectRepository(${EntityName}OrmEntity)
    private readonly repository: Repository<${EntityName}OrmEntity>,
  ) {}

  async findAll(): Promise<${EntityName}[]> {
    const entities = await this.repository.find();

    return entities.map(
      ${entityName} =>
        ${EntityName}PersistenceMapper.toDomain(${entityName}),
    );
  }

  async findById(id: string): Promise<${EntityName} | null> {
    const entity = await this.repository.findOne({
      where: { id },
    });

    if (!entity) {
      return null;
    }

    return ${EntityName}PersistenceMapper.toDomain(entity);
  }

  async save(
    ${entityName}: ${EntityName},
  ): Promise<void> {
    const entity =
      ${EntityName}PersistenceMapper.toPersistence(${entityName});

    await this.repository.save(entity);
  }

  async delete(
    ${entityName}: ${EntityName},
  ): Promise<void> {
    await this.repository.delete(${entityName}.getId());
  }
}
