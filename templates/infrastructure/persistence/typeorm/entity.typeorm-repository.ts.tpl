import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';

import { ${EntityName} } from '../../../domain/entities/${entityKebab}.entity';
import { ${EntityName}Repository } from '../../../domain/repositories/${entityKebab}.repository';

import { ${EntityName}PersistenceMapper } from '../mappers/${entityKebab}.persistence-mapper';
import { ${EntityName}OrmEntity } from './${entityKebab}.orm-entity';

@Injectable()
export class TypeOrm${EntityName}Repository extends ${EntityName}Repository {
  constructor(
    @InjectRepository(${EntityName}OrmEntity)
    private readonly repository: Repository<${EntityName}OrmEntity>,
  ) {
    super();
  }

  async save(entity: ${EntityName}): Promise<${EntityName}> {
    const orm = ${EntityName}PersistenceMapper.toOrm(entity);
    const saved = await this.repository.save(orm);

    return ${EntityName}PersistenceMapper.toDomain(saved);
  }

  async findById(id: string): Promise<${EntityName} | null> {
    const orm = await this.repository.findOne({
      where: { id },
    });

    if (!orm) {
      return null;
    }

    return ${EntityName}PersistenceMapper.toDomain(orm);
  }

  /*async findAll(): Promise<${EntityName}[]> {
    const items = await this.repository.find();

    return items.map((item) => ${EntityName}PersistenceMapper.toDomain(item));
  }
}*/
  async deleteById(id: string): Promise<void> {
    await this.repository.delete(id);
  }

async findAll(filters?: Record<string, unknown>): Promise<${EntityName}[]> {
  const entities = await this.repository.find(
    filters ? { where: filters } : {},
  );

  return entities.map(
    (entity) => ${EntityName}PersistenceMapper.toDomain(entity),
  );
}
