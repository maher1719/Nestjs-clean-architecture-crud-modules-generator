import { Create${EntityName}Command } from './create-${entityKebab}.command';
import { Create${EntityName}Handler } from './create-${entityKebab}.handler';
import { ${EntityName}Repository } from '../../../domain/repositories/${entityKebab}.repository';

describe('Create${EntityName}Handler', () => {
  let handler: Create${EntityName}Handler;
  let repository: jest.Mocked<${EntityName}Repository>;

  beforeEach(() => {
    repository = {
      findAll: jest.fn(),
      findById: jest.fn(),
      save: jest.fn(),
      delete: jest.fn(),
    };

    handler = new Create${EntityName}Handler(repository);
  });

  it('creates an ${entityName}', async () => {
    const command = new Create${EntityName}Command(
${createHandlerTestArguments}
    );

    const result = await handler.execute(command);

    expect(result).toBeInstanceOf(${EntityName});
    expect(repository.save).toHaveBeenCalledWith(result);
  });
});
