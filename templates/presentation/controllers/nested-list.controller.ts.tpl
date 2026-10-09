import { Controller, Get, Param } from '@nestjs/common';
import { ApiOperation, ApiTags } from '@nestjs/swagger';

import { List${EntityName}Query } from '../../application/queries/list-${entityKebab}/list-${entityKebab}.query';
import { List${EntityName}Handler } from '../../application/queries/list-${entityKebab}/list-${entityKebab}.handler';



@ApiTags('${parentRoute} > ${childRoute}')
@Controller('${parentRoute}/:${fkParam}/${childRoute}')
export class ${NestedControllerName} {
  constructor(
    private readonly listHandler: List${EntityName}Handler,
  ) {}

  @Get()
  @ApiOperation({ summary: 'List ${childRoute} belonging to a ${parentEntityLower}' })
  async findAllForParent(
    @Param('${fkParam}') ${fkParam}: string,
  ) {
    return this.listHandler.execute(
      new List${EntityName}Query({ filters: { ${fkField}: ${fkParam} } }),
    );
  }
}
