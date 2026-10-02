import { ${EntityName} } from '../../../domain/entities/${entityKebab}.entity';
import { ${EntityName}OrmEntity } from '../typeorm/${entityKebab}.orm-entity';

export class ${EntityName}PersistenceMapper {
  static toDomain(
    entity: ${EntityName}OrmEntity,
  ): ${EntityName} {
    return ${EntityName}.reconstitute({
${persistenceToDomainFields}
    });
  }

  static toPersistence(
    ${entityName}: ${EntityName},
  ): ${EntityName}OrmEntity {
    const entity = new ${EntityName}OrmEntity();

${domainToPersistenceFields}

    return entity;
  }
}
