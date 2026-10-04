${typeormImports}
${relationImports}

@Entity('${tableName}')
export class ${EntityName}OrmEntity {
  @PrimaryColumn('uuid')
  id: string;

${ormColumns}

${ormRelations}

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
