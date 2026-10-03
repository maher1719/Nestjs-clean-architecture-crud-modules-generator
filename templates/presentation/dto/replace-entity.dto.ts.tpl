import { ApiProperty } from '@nestjs/swagger';
import {
${replaceValidatorImports},
} from 'class-validator';

export class Replace${EntityName}Dto {
${replaceDtoFields}
}
