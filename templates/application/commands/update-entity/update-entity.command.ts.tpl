export class Update${EntityName}Command {
  constructor(
    public readonly id: string,
${updateCommandParameters}
  ) {}
}
