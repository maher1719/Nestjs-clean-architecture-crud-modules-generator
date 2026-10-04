import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
${moduleImports}
${nestedControllerImports}

@Module({
  imports: [
    TypeOrmModule.forFeature([${EntityName}OrmEntity]),
  ],
  controllers: [
    ${moduleControllers},
${nestedControllers}
  ],
  providers: [
${moduleProviders}
  ],
  exports: [
${moduleExports}
  ],
})
export class ${EntityName}Module {}
