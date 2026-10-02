${typeormImports}

${relationImports}

@Entity('${tableName}')
export class ${EntityName}OrmEntity {
  @PrimaryColumn('uuid')
  id!: string;

${ormColumns}

${ormRelations}

  @CreateDateColumn({ type: 'timestamptz' })
  createdAt!: Date;

  @UpdateDateColumn({ type: 'timestamptz' })
  updatedAt!: Date;
}
