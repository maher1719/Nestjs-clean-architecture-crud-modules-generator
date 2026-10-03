CREATE_DTO_TEMPLATE = """\
  import { ApiProperty } from '@nestjs/swagger';
import {
${createValidatorImports},
} from 'class-validator';
export class Create${EntityName}Dto {
${createDtoFields}
}
"""


UPDATE_DTO_TEMPLATE = """\
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import {
${updateValidatorImports},
} from 'class-validator';
export class Update${EntityName}Dto {
${updateDtoFields}
}
"""


CONTROLLER_TEMPLATE = """\
  import {
  Body,
  Controller,
  Delete,
  Get,
  Param,
  Post,
  Put,
  Patch,
} from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse } from '@nestjs/swagger';

import { Create${EntityName}Command } from '../../application/commands/create-${entityKebab}/create-${entityKebab}.command';
import { Create${EntityName}Handler } from '../../application/commands/create-${entityKebab}/create-${entityKebab}.handler';

import { Update${EntityName}Command } from '../../application/commands/update-${entityKebab}/update-${entityKebab}.command';
import { Update${EntityName}Handler } from '../../application/commands/update-${entityKebab}/update-${entityKebab}.handler';

import { Delete${EntityName}Command } from '../../application/commands/delete-${entityKebab}/delete-${entityKebab}.command';
import { Delete${EntityName}Handler } from '../../application/commands/delete-${entityKebab}/delete-${entityKebab}.handler';

import { Get${EntityName}Query } from '../../application/queries/get-${entityKebab}/get-${entityKebab}.query';
import { Get${EntityName}Handler } from '../../application/queries/get-${entityKebab}/get-${entityKebab}.handler';

import { List${EntityName}Query } from '../../application/queries/list-${entityKebab}/list-${entityKebab}.query';
import { List${EntityName}Handler } from '../../application/queries/list-${entityKebab}/list-${entityKebab}.handler';

import { Create${EntityName}Dto } from '../dto/create-${entityKebab}.dto';
import { Update${EntityName}Dto } from '../dto/update-${entityKebab}.dto';

@ApiTags('${moduleName}')
@Controller('${routeName}')
export class ${EntityName}Controller {
  constructor(
    private readonly createHandler: Create${EntityName}Handler,
    private readonly updateHandler: Update${EntityName}Handler,
    private readonly deleteHandler: Delete${EntityName}Handler,
    private readonly getHandler: Get${EntityName}Handler,
    private readonly listHandler: List${EntityName}Handler,
  ) {}

  @Post()
  @ApiOperation({ summary: 'Create a new ${entityName}' })
  @ApiResponse({ status: 201, description: 'The ${entityName} has been successfully created.' })
  async create(
    @Body() dto: Create${EntityName}Dto,
  ) {
    const command = new Create${EntityName}Command(
${createControllerArguments}
    );

    return this.createHandler.execute(command);
  }

  @Get()
  @ApiOperation({ summary: 'Get all ${moduleName}' })
  @ApiResponse({ status: 200, description: 'List of all ${moduleName}.' })
  async findAll() {
    return this.listHandler.execute(
      new List${EntityName}Query(),
    );
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get a ${entityName} by ID' })
  @ApiResponse({ status: 200, description: 'The ${entityName} details.' })
  @ApiResponse({ status: 404, description: '${EntityName} not found.' })
  async findOne(
    @Param('id') id: string,
  ) {
    return this.getHandler.execute(
      new Get${EntityName}Query(id),
    );
  }

  @Put(':id')
  @ApiOperation({ summary: 'Fully replace a ${entityName}' })
  @ApiResponse({ status: 200, description: 'The ${entityName} has been replaced.' })
  @ApiResponse({ status: 404, description: '${EntityName} not found.' })
  async replace(
    @Param('id') id: string,
    @Body() dto: Update${EntityName}Dto,
  ) {
    const command = new Update${EntityName}Command(
      id,
${updateControllerArguments}
    );

    return this.updateHandler.execute(command);
  }

  @Patch(':id')
  @ApiOperation({ summary: 'Partially update a ${entityName}' })
  @ApiResponse({ status: 200, description: 'The ${entityName} has been updated.' })
  @ApiResponse({ status: 404, description: '${EntityName} not found.' })
  async update(
    @Param('id') id: string,
    @Body() dto: Update${EntityName}Dto,
  ) {
    const command = new Update${EntityName}Command(
      id,
${updateControllerArguments}
    );

    return this.updateHandler.execute(command);
  }

  @Delete(':id')
  @ApiOperation({ summary: 'Delete a ${entityName}' })
  @ApiResponse({ status: 200, description: 'The ${entityName} has been deleted.' })
  @ApiResponse({ status: 404, description: '${EntityName} not found.' })
  async remove(
    @Param('id') id: string,
  ): Promise<void> {
    return this.deleteHandler.execute(
      new Delete${EntityName}Command(id),
    );
  }
}
"""


PRESENTATION_TEMPLATES = {
    "presentation/controllers/entity.controller.ts.tpl": CONTROLLER_TEMPLATE,
    "presentation/dto/create-entity.dto.ts.tpl": CREATE_DTO_TEMPLATE,
    "presentation/dto/update-entity.dto.ts.tpl": UPDATE_DTO_TEMPLATE,
}