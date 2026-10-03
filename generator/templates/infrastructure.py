ORM_ENTITY_TEMPLATE = """\
import {
  Column,
  CreateDateColumn,
  Entity,
  PrimaryColumn,
  UpdateDateColumn,
} from 'typeorm';
${typeormImports}

@Entity('${tableName}')
export class ${EntityName}OrmEntity {
  @PrimaryColumn('uuid')
  id: string;

${ormColumns}

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
"""


TYPEORM_REPOSITORY_TEMPLATE = """\
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

  async findAll(): Promise<${EntityName}[]> {
    const items = await this.repository.find();

    return items.map((item) => ${EntityName}PersistenceMapper.toDomain(item));
  }

  async deleteById(id: string): Promise<void> {
    await this.repository.delete(id);
  }
}
"""


PERSISTENCE_MAPPER_TEMPLATE = """\
import { ${EntityName} } from '../../../domain/entities/${entityKebab}.entity';
import { ${EntityName}OrmEntity } from '../typeorm/${entityKebab}.orm-entity';

export class ${EntityName}PersistenceMapper {
  static toDomain(
    orm: ${EntityName}OrmEntity,
  ): ${EntityName} {
    return ${EntityName}.reconstitute({
      id: orm.id,
${ormToDomainFields}
      createdAt: orm.createdAt,
      updatedAt: orm.updatedAt,
    });
  }

  static toOrm(
    entity: ${EntityName},
  ): ${EntityName}OrmEntity {
    const orm = new ${EntityName}OrmEntity();

    orm.id = entity.id;
${domainToOrmFields}
    orm.createdAt = entity.createdAt;
    orm.updatedAt = entity.updatedAt;

    return orm;
  }
}
"""


INFRASTRUCTURE_TEMPLATES = {
    "infrastructure/persistence/typeorm/entity.orm-entity.ts.tpl": ORM_ENTITY_TEMPLATE,
    "infrastructure/persistence/mappers/entity.persistence-mapper.ts.tpl": PERSISTENCE_MAPPER_TEMPLATE,
    "infrastructure/persistence/typeorm/entity.typeorm-repository.ts.tpl": TYPEORM_REPOSITORY_TEMPLATE,
}