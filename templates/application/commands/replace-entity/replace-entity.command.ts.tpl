export class Replace${EntityName}Command {
  constructor(
    public readonly id: string,
${replaceCommandParameters}
  ) {}
}
