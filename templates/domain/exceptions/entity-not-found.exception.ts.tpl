export class ${EntityName}NotFoundException extends Error {
  constructor() {
    super('${EntityName} not found.');
    this.name = '${EntityName}NotFoundException';
  }
}
