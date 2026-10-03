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
