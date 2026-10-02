import { ${EntityName} } from '../entities/${entityKebab}.entity';

export abstract class ${EntityName}Repository {
  abstract findAll(): Promise<${EntityName}[]>;
  abstract findById(id: string): Promise<${EntityName} | null>;
  abstract save(${entityName}: ${EntityName}): Promise<void>;
  abstract delete(${entityName}: ${EntityName}): Promise<void>;
}
