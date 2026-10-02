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
