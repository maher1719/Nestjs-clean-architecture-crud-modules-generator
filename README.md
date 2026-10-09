# 🏗️ NestJS Clean Architecture CRUD Generator

> **Stop writing boilerplate.** Generate production-grade, strictly-typed **NestJS** modules following **Clean Architecture**, **Domain-Driven Design (DDD)**, and **CQRS** from a single YAML file.

Define your entity, run one command, and get a fully structured module with domain logic, CQRS handlers, TypeORM persistence, DTO validation, Swagger documentation, and REST controllers.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🏛️ **Clean Architecture** | Strict `domain` / `application` / `infrastructure` / `presentation` layering. |
| ⚡ **CQRS** | Separate Commands & Queries with dedicated Handlers. |
| 🔗 **All 4 Relations** | `many-to-one`, `one-to-many`, `one-to-one`, `many-to-many` with proper FK ownership. |
| 🧩 **Aggregates (DDD)** | Parent validation, cascade enforcement, and auto-generated nested read routes. |
| 🔄 **PUT vs PATCH** | Strict separation between full `Replace` and partial `Update`. |
| 📊 **Production Lists** | Built-in Pagination, Whitelisted Filtering, and Sorting (v3). |
| 📄 **Swagger & Validation** | Auto-generated `class-validator` DTOs and `@nestjs/swagger` decorators. |
| 🗂️ **Module Manifest** | `.generator.manifest.json` tracks every generated module for easy retrieval. |
| 📦 **Bulk Generation** | Point at a folder of YAMLs and generate your entire domain at once. |
| 🔒 **Idempotent** | Safe re-runs; never duplicates imports in `app.module.ts`. |

---

## 🚀 Quick Start

### 1. Define your entity in YAML

```yaml
# modules/comment.yml
module: comments
parent: posts                       # Marks this as an aggregate child of 'posts'

entity:
  name: Comment
  table: comments
  fields:
    - name: text
      type: string
      sortable: true                # Allow sorting by this field
    - name: postId
      type: uuid
      filterable: true              # Allow filtering by this field
    - name: authorId
      type: uuid
      filterable: true

relations:
  # Aggregate parent (must be cascade + non-nullable)
  - name: post
    type: many-to-one
    target: Post
    targetModule: posts
    foreignKey: postId
    nullable: false
    onDelete: cascade

  # Standard association
  - name: author
    type: many-to-one
    target: User
    targetModule: users
    foreignKey: authorId
    nullable: false
    onDelete: restrict

operations:
  - create
  - list
  - get
  - update
  - delete
```

### 2. Generate

```bash
# Generate a single module
python -m generator.structure.cli modules/comment.yml --src src/

# Bulk generate an entire folder
python -m generator.structure.cli modules/ --src src/ --force
```

### 3. Enjoy your API 🎉

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/comments` | Create a comment |
| `GET` | `/comments` | List all (supports `?page=1&limit=10&sortBy=text`) |
| `GET` | `/comments?postId=<uuid>` | Filter by foreign key |
| `GET` | `/comments/:id` | Get one comment |
| `PATCH` | `/comments/:id` | Partial update |
| `PUT` | `/comments/:id` | Full replace |
| `DELETE` | `/comments/:id` | Delete |
| `GET` | `/posts/:postId/comments` | **Nested aggregate read route** (auto-generated) |

---

## 📖 YAML Configuration Reference

### Field Types & List Options

| Type | TS Type | TypeORM | Validator | List Options |
|---|---|---|---|---|
| `string` | `string` | `varchar` | `@IsString` | `sortable`, `filterable` |
| `number` | `number` | `integer` | `@IsNumber` | `sortable`, `filterable` |
| `boolean` | `boolean` | `boolean` | `@IsBoolean` | `filterable` |
| `date` | `Date` | `timestamptz` | `@IsDateString` | `sortable`, `filterable` |
| `uuid` | `string` | `uuid` | `@IsUUID` | `filterable` |

*Note: `id`, `createdAt`, and `updatedAt` are managed automatically and are sortable by default.*

### Relationships

#### `many-to-one` (Owning side - holds the FK)
```yaml
- name: author
  type: many-to-one
  target: User
  targetModule: users
  foreignKey: authorId
  nullable: false
  onDelete: restrict # restrict | cascade | set-null | no-action
```

#### `one-to-many` (Inverse side)
```yaml
- name: comments
  type: one-to-many
  target: Comment
  targetModule: comments
  mappedBy: author # Must match the child's many-to-one relation name
```

#### `one-to-one` (Owning side - FK is marked UNIQUE)
```yaml
- name: profile
  type: one-to-one
  target: Profile
  targetModule: profiles
  foreignKey: profileId
  nullable: true
  onDelete: set-null
```

#### `many-to-many` (Junction table)
```yaml
- name: tags
  type: many-to-many
  target: Tag
  targetModule: tags
  joinTable: post_tags
  joinColumn: post_id
  inverseJoinColumn: tag_id
```

---

## 💻 CLI Usage

```bash
python -m generator.structure.cli <path> [options]
```

**Arguments:**
* `<path>`: Path to a single `.yml` file, or a directory for bulk generation.

**Options:**
| Flag | Default | Description |
|---|---|---|
| `--src` | `src` | Root directory where modules are generated. |
| `--templates` | `templates` | Directory containing the `.tpl` template files. |
| `--app-module` | `<src>/app.module.ts` | Path to app.module.ts for auto-registration. |
| `--project-root` | `.` | Where `.generator.manifest.json` is stored. |
| `--force` | `False` | Overwrite existing generated files. |
| `--dry-run` | `False` | Validate and print output without writing files. |
| `--fail-fast` | `False` | Stop bulk generation on the first error. |

---

## 🗂️ The Module Manifest

Every successful generation upserts an entry into **`.generator.manifest.json`** at the project root. 

**Commit this file to Git.** It serves as the team-visible inventory of everything the generator has produced, preventing modules from "popping out of nowhere" and enabling future cross-module validation.

---

## 🧠 Generator Architecture

The generator is a modular Python package. Templates (`.tpl` files) are edited directly, and the Python code handles parsing, validation, and rendering.

```text
generator/
├── structure/
│   ├── cli.py                 # Entry point (single + bulk)
│   ├── config_loader.py       # YAML loading + aggregate validation
│   ├── generator.py           # Orchestrates file writing
│   ├── context.py             # Builds the template context
│   ├── output_mapper.py       # Template → output path mapping
│   ├── manifest.py            # .generator.manifest.json upsert
│   ├── app_module_updater.py  # Idempotent app.module.ts registration
│   ├── fields/                # Field builder package
│   │   ├── normalization.py   #   normalize fields/relations
│   │   ├── types.py           #   ts_type, typeorm_type
│   │   ├── domain.py          #   entity/command/handler builders
│   │   ├── dto.py             #   DTO + validator + swagger builders
│   │   ├── orm.py             #   ORM columns + imports
│   │   ├── mapping.py         #   domain ↔ ORM field mapping
│   │   └── registry.py        #   build_field_context orchestrator
│   └── relations/             # Relation builders
│       ├── many_to_one.py
│       ├── one_to_many.py
│       ├── one_to_one.py
│       ├── many_to_many.py
│       └── registry.py        # relation dispatcher
└── templates/                 # .tpl template sources (edit these directly!)
```

---

## 🗺️ Roadmap

- [x] **v1:** Clean Architecture CRUD, CQRS, TypeORM, 4 Relation Types.
- [x] **v2:** Aggregates, Nested Reads, Manifest, Bulk Generation, Idempotent Registration.
- [x] **v3:** Pagination, Whitelisted Filtering, Sorting.


---

## 📄 License

This project is licensed under the **AGPL-3.0 License**.

**Enterprise / Commercial Use:** If you wish to use this generator in proprietary, closed-source products without the AGPL open-source obligations, a commercial license is available. Please contact the maintainer for details.

---

*Built to eliminate boilerplate so you can focus on your domain.*