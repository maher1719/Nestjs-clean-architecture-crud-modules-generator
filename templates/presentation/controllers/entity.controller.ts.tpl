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

import { ApiTags } from '@nestjs/swagger';

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
  async create(
    @Body() dto: Create${EntityName}Dto,
  ) {
    const command = new Create${EntityName}Command(
${createControllerArguments}
    );

    return this.createHandler.execute(command);
  }

  @Get()
  async findAll() {
    return this.listHandler.execute(
      new List${EntityName}Query(),
    );
  }

  @Get(':id')
  async findOne(
    @Param('id') id: string,
  ) {
    return this.getHandler.execute(
      new Get${EntityName}Query(id),
    );
  }

/*
  @Put(':id')
  async update(
    @Param('id') id: string,
    @Body() dto: Update${EntityName}Dto,
  ) {
    const command = new Update${EntityName}Command(
      id,
${updateControllerArguments}
    );

    return this.updateHandler.execute(command);
  }*/


  @Patch(':id')
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
  async remove(
    @Param('id') id: string,
  ): Promise<void> {
    return this.deleteHandler.execute(
      new Delete${EntityName}Command(id),
    );
  }
}
