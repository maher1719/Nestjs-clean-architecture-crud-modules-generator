ENTITY_ENTITY_TEMPLATE = """\
${entityImports}

export interface ${EntityName}Props {
  id: string;
${entityProps}
  createdAt: Date;
  updatedAt: Date;
}

export class ${EntityName} {
  private constructor(
    private props: ${EntityName}Props,
  ) {}

  static create(
${createEntityParameters}
  ): ${EntityName} {
    const now = new Date();

    return new ${EntityName}({
      id: randomUUID(),
${createEntityFields}
      createdAt: now,
      updatedAt: now,
    });
  }

  static reconstitute(
    props: ${EntityName}Props,
  ): ${EntityName} {
    return new ${EntityName}(props);
  }

${updateMethods}

${getters}
}
"""


ENTITY_REPOSITORY_TEMPLATE = """\
import { ${EntityName} } from '../entities/${entityKebab}.entity';

export abstract class ${EntityName}Repository {
  abstract save(entity: ${EntityName}): Promise<${EntityName}>;
  abstract findById(id: string): Promise<${EntityName} | null>;
  //abstract findAll(): Promise<${EntityName}[]>;
  abstract findAll(filters?: Record<string, unknown>): Promise<${EntityName}[]>;
  abstract deleteById(id: string): Promise<void>;
}
"""


DOMAIN_TEMPLATES = {
    "domain/entities/entity.entity.ts.tpl": ENTITY_ENTITY_TEMPLATE,
    "domain/repositories/entity.repository.ts.tpl": ENTITY_REPOSITORY_TEMPLATE,
}