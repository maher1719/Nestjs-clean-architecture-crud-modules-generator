import { ${EntityName} } from '../entities/${entityKebab}.entity';
import { ListOptions, Paginated } from './list-options';

export abstract class ${EntityName}Repository {
  abstract save(entity: ${EntityName}): Promise<${EntityName}>;
  abstract findAll(options?: ListOptions): Promise<Paginated<${EntityName}>>;
  abstract findById(id: string): Promise<${EntityName} | null>;
  //abstract findAll(filters?: Record<string, unknown>): Promise<${EntityName}[]>;
  abstract deleteById(id: string): Promise<void>;
}
