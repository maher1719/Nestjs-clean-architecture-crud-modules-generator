import { ApiProperty } from '@nestjs/swagger';

import {
  ${createValidatorImports},
} from 'class-validator';

export class Create${EntityName}Dto {
${createDtoFields}
}
