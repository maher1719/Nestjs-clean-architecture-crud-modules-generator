MODULE_TEMPLATE = """\
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
${moduleImports}

@Module({
  imports: [
    TypeOrmModule.forFeature([${EntityName}OrmEntity]),
  ],
  controllers: [${moduleControllers}],
  providers: [
${moduleProviders}
  ],
  exports: [
${moduleExports}
  ],
})
export class ${EntityName}Module {}
"""


MODULE_TEMPLATES = {
    "module.ts.tpl": MODULE_TEMPLATE,
}