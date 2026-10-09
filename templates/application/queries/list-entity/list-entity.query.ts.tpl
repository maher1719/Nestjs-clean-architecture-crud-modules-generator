import { ListOptions } from '../../../domain/repositories/list-options';

export class List${EntityName}Query {
  constructor(
    public readonly options: ListOptions = {},
  ) {}
}