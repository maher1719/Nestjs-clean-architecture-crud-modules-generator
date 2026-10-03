import { ${EntityName} } from '../entities/${entityKebab}.entity';

export abstract class ${EntityName}Repository {
  abstract save(entity: ${EntityName}): Promise<${EntityName}>;
  abstract findById(id: string): Promise<${EntityName} | null>;
  abstract findAll(): Promise<${EntityName}[]>;
  abstract deleteById(id: string): Promise<void>;
}
