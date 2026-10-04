from pathlib import Path
from typing import Any, Dict

from ..filesystem import ensure_directory
from .app_module_updater import update_app_module # <-- IMPORT THIS
from .config_loader import validate_config
from .context import build_context,build_nested_controller_specs,build_nested_module_context
from .output_mapper import build_output_mapping
from .rendering import load_template, render_template


def generate_module(
    config: Dict[str, Any],
    *,
    templates_dir: Path,
    src_dir: Path,
    app_module_path: Path, # <-- ADD THIS PARAMETER
    dry_run: bool = False,
    force: bool = False,
) -> None:
    validate_config(config)

    entity = config["entity"]

    entity_name = entity["name"]
    module_name = config["module"]

    context = build_context(config)


    nested_specs = build_nested_controller_specs(config, context)
    context.update(build_nested_module_context(nested_specs))


    output_mapping = build_output_mapping(
        entity_name=entity_name,
        module_name=module_name,
    )

    module_root = src_dir / module_name

    if dry_run:
        print(f"[dry-run] module: {module_root}")
    else:
        ensure_directory(module_root)

    if not templates_dir.exists():
        raise FileNotFoundError(f"Templates directory not found: {templates_dir}")

    for template_path, output_path in output_mapping.items():
        template_content = load_template(
            templates_dir=templates_dir,
            template_path=template_path,
        )

        rendered = render_template(
            template_content=template_content,
            context=context,
        )

        destination = module_root / output_path

        if dry_run:
            print(f"[dry-run] {destination}")
            continue

        ensure_directory(destination.parent)

        if destination.exists() and not force:
            print(f"[skipped] {destination}")
            continue

        destination.write_text(
            rendered,
            encoding="utf-8",
        )

        print(f"[created] {destination}")

    module_file_path = module_root / f"{module_name}.module.ts"
    module_class_name = f"{entity_name}Module"
    for spec in nested_specs:
        template = load_template(
            templates_dir,
            "presentation/controllers/nested-list.controller.ts.tpl",
        )
        rendered = render_template(template, spec["context"])
        destination = module_root / spec["output_path"]

        if dry_run:
            print(f"[dry-run] {destination}")
            continue

        ensure_directory(destination.parent)
        if destination.exists() and not force:
            print(f"[skipped] {destination}")
            continue

        destination.write_text(rendered, encoding="utf-8")
        print(f"[created] {destination}")
    update_app_module(
        app_module_path=app_module_path,
        module_file_path=module_file_path,
        module_class_name=module_class_name,
        module_name=module_name,
        dry_run=dry_run,
    )