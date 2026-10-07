# 🏗️ NestJS Clean Architecture CRUD Modules Generator

> A Python-powered code generator that scaffolds production-grade **NestJS** modules following **Clean Architecture**, **Domain-Driven Design (DDD)**, and **CQRS** — all from a simple YAML definition.

Stop writing boilerplate. Define your entity in YAML, run one command, and get a fully-structured, typed, documented module with domain logic, CQRS handlers, TypeORM persistence, DTO validation, Swagger docs, and REST controllers.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🏛️ **Clean Architecture** | Strict `domain` / `application` / `infrastructure` / `presentation` layering |
| ⚡ **CQRS** | Separate commands & queries with dedicated handlers |
| 📝 **YAML-driven** | Declarative entity definitions — no code to write |
| 🔗 **All 4 relation types** | `many-to-one`, `one-to-many`, `one-to-one`, `many-to-many` |
| 🧩 **Aggregate support** | Parent validation, cascade rules, nested read routes |
| 🔁 **PUT vs PATCH** | Full `replace` operation distinct from partial `update` |
| 📄 **Auto DTOs + validation** | `class-validator` decorators generated per field type |
| 📚 **Swagger ready** | `@ApiProperty` / `@ApiTags` generated automatically |
| 🗂️ **Module manifest** | `.generator.manifest.json` tracks every generated module |
| 📦 **Bulk generation** | Generate an entire folder of YAMLs in one command |
| 🔒 **Idempotent registration** | Safe re-runs — never duplicates `app.module.ts` imports |

---

## 🏛️ What Gets Generated

For each YAML definition, the generator produces a complete Clean Architecture module:

```
src/modules/<module>/
├── domain/
│   ├── entities/            # Rich domain entity (props, factory, getters, updaters)
│   ├── repositories/        # Abstract repository port
│   └── exceptions/          # Domain exceptions (e.g. NotFoundException)
├── application/
│   ├── commands/            # CQRS write side
│   │   ├── create-<entity>/
│   │   ├── update-<entity>/
│   │   ├── replace-<entity>/
│   │   └── delete-<entity>/
│   └── queries/             # CQRS read side
│       ├── get-<entity>/
│       └── list-<entity>/
├── infrastructure/
│   └── persistence/
│       ├── typeorm/         # ORM entity (columns + relations)
│       ├── mappers/         # Domain ↔ ORM mappers
│       └── repositories/    # TypeORM repository adapter
├── presentation/
│   ├── controllers/         # REST controller (+ nested read routes)
│   ├── dto/                 # Create / Update / Replace DTOs
│   └── filters/             # Exception filters
└── <module>.module.ts       # NestJS module wiring
```

---

## 📦 Installation

```bash
# Clone the generator
git clone https://github.com/maher1719/Nestjs-clean-architecture-crud-modules-generator.git
cd Nestjs-clean-architecture-crud-modules-generator

# Install Python dependencies
pip install pyyaml
```

> **Requirements:** Python 3.10+ and an existing NestJS project with TypeORM, `class-validator`, and `@nestjs/swagger`.

---

## 🚀 Quick Start

### 1. Define your entity in YAML

```yaml
# modules/comment.yml
module: comments
parent: posts                       # marks this as an aggregate child
entity:
  name: Comment
  table: comments
  fields:
    - name: text
      type: string
    - name: postId
      type: uuid
    - name: authorId
      type: uuid

relations:
  - name: post
    type: many-to-one
    target: Post
    targetModule: posts
    foreignKey: postId
    nullable: false
    onDelete: cascade

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
python -m generator.structure.cli modules/comment.yml --src src
```

### 3. Done 🎉

You now have a full module with REST endpoints:

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/comments` | Create a comment |
| `GET` | `/comments` | List all comments |
| `GET` | `/comments/:id` | Get one comment |
| `PATCH` | `/comments/:id` | Partial update |
| `PUT` | `/comments/:id` | Full replace |
| `DELETE` | `/comments/:id` | Delete |
| `GET` | `/posts/:postId/comments` | Nested read (auto-generated) |

---

## 📖 YAML Configuration Reference

### Top-level keys

| Key | Type | Description |
|---|---|---|
| `module` | `string` | Module/folder name (plural, kebab) |
| `parent` | `string?` | Parent module name → marks an **aggregate child** |
| `entity` | `object` | Entity definition (`name`, `table`, `fields`) |
| `relations` | `list?` | Relationships to other entities |
| `operations` | `list` | Which endpoints to generate |

### Field types

| Type | TypeScript | TypeORM | Validator |
|---|---|---|---|
| `string` | `string` | `varchar(255)` | `@IsString` |
| `number` | `number` | `integer` | `@IsNumber` |
| `boolean` | `boolean` | `boolean` | `@IsBoolean` |
| `date` | `Date` | `timestamptz` | `@IsDateString` |
| `uuid` | `string` | `uuid` | `@IsUUID` |

Reserved field names (auto-managed): `id`, `createdAt`, `updatedAt`.

### Operations

`create`, `list`, `get`, `update`, `delete`, `replace`

---

## 🔗 Relationships

All four TypeORM relation types are supported. Relations generate ORM decorators, imports, and — where relevant — nested read routes.

### `many-to-one` (owning side — holds the FK)

```yaml
relations:
  - name: post
    type: many-to-one
    target: Post
    targetModule: posts
    foreignKey: postId
    nullable: false
    onDelete: cascade        # restrict | cascade | set-null | no-action
```

### `one-to-many` (inverse side — no FK)

```yaml
relations:
  - name: comments
    type: one-to-many
    target: Comment
    targetModule: comments
    mappedBy: post           # must match the child's many-to-one name
```

### `one-to-one` (owning side — FK marked `unique`)

```yaml
relations:
  - name: profile
    type: one-to-one
    target: Profile
    targetModule: profiles
    foreignKey: profileId
    nullable: true
    onDelete: set-null
```

### `many-to-many` (junction table)

```yaml
relations:
  - name: tags
    type: many-to-many
    target: Tag
    targetModule: tags
    joinTable: post_tags
    joinColumn: post_id
    inverseJoinColumn: tag_id
```

---

## 🧩 Aggregates

Mark a module as an **aggregate child** with the `parent` key:

```yaml
module: comments
parent: posts
```

The generator then **validates** the aggregate relationship:
- ✅ A `many-to-one` relation targeting the parent must exist
- ✅ That relation must use `onDelete: cascade`
- ✅ That relation must be non-nullable

It also auto-generates a **nested read route** on the child (e.g. `GET /posts/:postId/comments`) so children can be listed through their parent.

---

## 💻 CLI Usage

```bash
# Generate a single module
python -m generator.structure.cli modules/profile.yml --src src

# Bulk-generate every YAML in a folder
python -m generator.structure.cli modules/ --src src

# Preview without writing files (also skips the manifest)
python -m generator.structure.cli modules/ --src src --dry-run

# Overwrite existing generated files
python -m generator.structure.cli modules/profile.yml --src src --force

# Stop bulk generation at the first error
python -m generator.structure.cli modules/ --src src --fail-fast

# Custom app.module.ts location & project root
python -m generator.structure.cli modules/profile.yml \
  --src src \
  --app-module src/app.module.ts \
  --project-root .
```

### Flags

| Flag | Default | Description |
|---|---|---|
| `config` | — | YAML file **or** folder (auto-detected) |
| `--src` | `src` | Where modules are generated |
| `--templates` | `templates` | Directory of `.tpl` template files |
| `--app-module` | `<src>/app.module.ts` | app.module.ts for auto-registration |
| `--project-root` | CWD | Where `.generator.manifest.json` lives |
| `--dry-run` | off | Validate/render without writing |
| `--force` | off | Overwrite existing files |
| `--fail-fast` | off | Stop bulk on first error |

---

## 🗂️ The Module Manifest

Every successful generation upserts an entry into **`.generator.manifest.json`** at the project root. It records each module's metadata for retrieval, validation, and future reconciliation.

```json
{
  "schemaVersion": 1,
  "generatorVersion": "v2",
  "modules": {
    "comments": {
      "entity": "Comment",
      "table": "comments",
      "configPath": "modules/comment.yml",
      "outputPath": "src/modules/comments",
      "moduleFile": "src/modules/comments/comments.module.ts",
      "parent": "posts",
      "relations": [
        { "type": "many-to-one", "target": "Post", "targetModule": "posts" }
      ],
      "operations": ["create", "list", "get", "update", "delete"],
      "generatedAt": "2026-03-15T12:00:00+00:00"
    }
  }
}
```

> 📌 **Commit this file.** It's the team-visible inventory of everything the generator has produced — no modules "popping out of nowhere."

---

## 🧠 Generator Architecture

The generator itself is a modular Python package:

```
generator/
├── structure/
│   ├── cli.py                 # Entry point (single + bulk)
│   ├── config_loader.py       # YAML loading + validation
│   ├── generator.py           # Orchestrates generation
│   ├── context.py             # Builds the template context
│   ├── output_mapper.py       # Template → output path mapping
│   ├── rendering.py           # Template rendering
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
└── templates/                 # .tpl template sources
```

---

## 🗺️ Roadmap

### ✅ v1 — Foundations
Clean Architecture CRUD, CQRS, TypeORM, all 4 relation types, Swagger, validation.

### ✅ v2 — Aggregates & Tooling
`replace`/PUT operation, parent validation, nested read routes, `fields/` package split, module manifest, bulk generation, idempotent `app.module.ts` registration.

### 🔜 v3 — List Query Enhancements
- **Pagination** — `?page=2&limit=20` with a `{ data, total, page, limit }` response
- **Filtering** — whitelisted query-param filters
- **Sorting** — `?sortBy=createdAt&order=desc`

### 🔮 v4 — Embedding
- `?include=comments` to embed related aggregates in responses

---

## 📄 License

This project is licensed under the **AGPL-3.0 License**.

**Enterprise / commercial use:** If you wish to use this generator in proprietary, closed-source products without the AGPL open-source obligations, a commercial license is available. Contact the maintainer for details.

---

## 🙌 Acknowledgements

Built with a focus on clean, maintainable code generation — so you can focus on your domain, not the boilerplate.

---

*Made with ❤️ by [maher1719](https://github.com/maher1719)*