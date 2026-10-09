import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { ${EntityName} } from '../../../domain/entities/${entityKebab}.entity';
import { ${EntityName}Repository } from '../../../domain/repositories/${entityKebab}.repository';
import { ${EntityName}PersistenceMapper } from '../mappers/${entityKebab}.persistence-mapper';
import { ${EntityName}OrmEntity } from './${entityKebab}.orm-entity';
import { ListOptions, Paginated } from '../../../domain/repositories/list-options';


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

  async deleteById(id: string): Promise<void> {
    await this.repository.delete(id);
  }

  async findAll(
    options: ListOptions = {},
  ): Promise<Paginated<${EntityName}>> {
    const page = options.page ?? 1;
    const limit = options.limit ?? 20;
    const sortBy = options.sortBy ?? 'createdAt';
    const order = options.order ?? 'DESC';

    const [entities, total] = await this.repository.findAndCount({
      where: options.filters ?? {},
      order: { [sortBy]: order },
      skip: (page - 1) * limit,
      take: limit,
    });

    return {
      data: entities.map(
        ${entityName} =>
          ${EntityName}PersistenceMapper.toDomain(${entityName}),
      ),
      total,
      page,
      limit,
    };
  }
}
