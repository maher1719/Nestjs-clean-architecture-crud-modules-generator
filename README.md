# 🏗️ NestJS Clean Architecture CRUD Modules Generator

A Python-based CLI tool that automatically scaffolds complete **NestJS modules** following **Clean Architecture**, **Domain-Driven Design (DDD)**, and **CQRS** principles from a simple YAML configuration file.

Stop writing repetitive boilerplate for your enterprise NestJS applications. Define your entities in YAML, and let this tool generate the Domain, Application, Infrastructure, and Presentation layers for you—complete with Swagger support!

## ✨ Features

- **Clean Architecture & DDD:** Generates strictly separated layers (`domain`, `application`, `infrastructure`, `presentation`).
- **CQRS Pattern:** Automatically creates Command and Query handlers for all CRUD operations.
- **TypeORM Integration:** Scaffolds ORM entities, repositories, and mappers.
- **Relational Support:** Handles Foreign Keys and relations (e.g., Many-to-One) across different modules.
- **Swagger Ready:** Controllers are pre-configured with `@ApiTags` for instant API documentation.
- **Safe Generation:** Includes a `--dry-run` flag to preview file structures without overwriting existing code.

---

## 📦 Prerequisites

- **Python 3.8+** (to run the generator scripts)
- An existing **NestJS** project with `@nestjs/typeorm`, `typeorm`, and `@nestjs/swagger` installed.

---

## 🚀 Installation & Setup

1. Clone this repository into your workspace (or add it as a dev tool):
   ```bash
   git clone https://github.com/maher1719/Nestjs-clean-architecture-crud-modules-generator.git
   cd Nestjs-clean-architecture-crud-modules-generator
   ```

2. (Optional) Install Python dependencies if a `requirements.txt` is provided:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🛠️ Usage

Run the `create_structure.py` script and pass the path to your YAML configuration file.

### Standard Generation
```bash
python create_structure.py path/to/your/module.yml
```

### Dry Run (Preview Only)
Use `--dry-run` to validate your YAML and see which files will be created without actually writing to the disk:
```bash
python create_structure.py path/to/your/module.yml --dry-run
```

---

## 📄 YAML Configuration Examples

The generator relies on a YAML file to define the module structure, entity fields, relations, and allowed operations.

### Example 1: Basic Module (`organization.yml`)

```yaml
module: organizations
entity:
  name: Organization
  table: organizations
  fields:
    - name: name
      type: string
      orm_type: varchar
      length: 255
operations:
  - create
  - list
  - get
  - update
  - delete
```

### Example 2: Module with Relations (`employee.yml`)

This example demonstrates how to link entities across different modules using foreign keys.

```yaml
module: employees
entity:
  name: Employees
  table: employees
  fields:
    - name: organizationId
      type: uuid
    - name: firstName
      type: string
    - name: lastName
      type: string
    - name: email
      type: string

relations:
  - name: organization
    type: many-to-one
    target: Organization
    targetModule: organizations
    foreignKey: organizationId
    nullable: false
    onDelete: restrict

operations:
  - create
  - list
  - get
  - update
  - delete
```

### Configuration Schema Breakdown:
| Key | Description |
| :--- | :--- |
| `module` | The NestJS module name (used for folder and routing naming). |
| `entity.name` | The name of the Domain Entity class. |
| `entity.table` | The database table name. |
| `fields` | Array of properties for the entity. Supports standard types (`string`, `uuid`, `number`, `boolean`) and TypeORM specific overrides (`orm_type`, `length`). |
| `relations` | Defines TypeORM relationships (`many-to-one`, `one-to-many`, etc.) and maps them to target modules. |
| `operations` | Whitelist of CQRS operations to generate (`create`, `list`, `get`, `update`, `delete`). |

---

## 📂 Generated Directory Structure

When you run the generator, it creates the following Clean Architecture folder structure inside your NestJS `src/` directory:

```text
📁 src/
 ┣ 📁 [module_name]/
 ┃ ┣ 📁 application/
 ┃ ┃ ┣ 📁 commands/       # CQRS Commands (Create, Update, Delete)
 ┃ ┃ ┗ 📁 queries/        # CQRS Queries (Get, List)
 ┃ ┣ 📁 domain/
 ┃ ┃ ┣ 📁 entities/       # DDD Entities (Props, Private Constructors)
 ┃ ┃ ┗ 📁 repositories/   # Repository Interfaces
 ┃ ┣ 📁 infrastructure/
 ┃ ┃ ┗ 📁 persistence/    # TypeORM Entities, Mappers, and Repository Implementations
 ┃ ┣ 📁 presentation/
 ┃ ┃ ┣ 📁 controllers/    # NestJS Controllers (with Swagger)
 ┃ ┃ ┗ 📁 dto/            # Data Transfer Objects (Validation)
 ┃ ┗ 📄 [module_name].module.ts  # NestJS Module Definition
```

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for new field types, relation types, or want to add support for other ORMs (like Prisma or Mongoose), feel free to open an Issue or submit a Pull Request.

---

## 📝 License

This project is licensed under the **AGPL-3.0 License**. See the [LICENSE](LICENSE) file for details.

---

*Built with ❤️ by [Maher](https://github.com/maher1719) for the NestJS community.*

