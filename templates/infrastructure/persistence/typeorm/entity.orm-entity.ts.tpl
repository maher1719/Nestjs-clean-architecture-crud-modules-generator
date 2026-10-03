import {
  Column,
  CreateDateColumn,
  Entity,
  PrimaryColumn,
  UpdateDateColumn,
} from 'typeorm';
${typeormImports}

@Entity('${tableName}')
export class ${EntityName}OrmEntity {
  @PrimaryColumn('uuid')
  id: string;

${ormColumns}

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
