import { ApiProperty } from '@nestjs/swagger';
import {
${updateValidatorImports},
} from 'class-validator';
export class Update${EntityName}Dto {
${updateDtoFields}
}
