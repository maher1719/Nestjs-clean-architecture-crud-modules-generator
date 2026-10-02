import {
  ArgumentsHost,
  Catch,
  ExceptionFilter,
  HttpStatus,
} from '@nestjs/common';

import { ${EntityName}NotFoundException } from '../../domain/exceptions/${entityKebab}-not-found.exception';

@Catch(${EntityName}NotFoundException)
export class ${EntityName}ExceptionFilter
  implements ExceptionFilter
{
  catch(
    exception: ${EntityName}NotFoundException,
    host: ArgumentsHost,
  ): void {
    const response = host.switchToHttp().getResponse();

    response.status(HttpStatus.NOT_FOUND).json({
      statusCode: HttpStatus.NOT_FOUND,
      message: exception.message,
    });
  }
}
