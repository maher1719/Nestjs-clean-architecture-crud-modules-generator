"""Command-line interface for the module generator."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple

from .config_loader import load_config
from .generator import generate_module
from .manifest import build_module_entry, upsert_module


YAML_SUFFIXES = {".yml", ".yaml"}


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def discover_yaml_files(folder: Path) -> List[Path]:
    """Top-level YAML files in `folder`, sorted for deterministic order."""
    return sorted(
        path for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in YAML_SUFFIXES
    )


# ---------------------------------------------------------------------------
# Single-module generation (with manifest upsert)
# ---------------------------------------------------------------------------

def generate_one(
    config_path: Path,
    *,
    templates_dir: Path,
    src_dir: Path,
    app_module_path: Path,
    project_root: Path,
    dry_run: bool,
    force: bool,
) -> str:
    """Generate one module and record it in the manifest. Returns module name."""
    config = load_config(config_path)

    generate_module(
        config,
        templates_dir=templates_dir,
        src_dir=src_dir,
        app_module_path=app_module_path,   # <-- ADD THIS
        dry_run=dry_run,
        force=force,
    )

    module_name = config["module"]

    if not dry_run:
        output_path = src_dir / module_name
        entry = build_module_entry(config, config_path, output_path, project_root)
        upsert_module(project_root, module_name, entry)

    return module_name

# ---------------------------------------------------------------------------
# Bulk generation
# ---------------------------------------------------------------------------

def generate_bulk(
    folder: Path,
    *,
    templates_dir: Path,
    src_dir: Path,
    app_module_path: Path,          # <-- ADD THIS
    project_root: Path,
    dry_run: bool,
    force: bool,
    fail_fast: bool,
) -> Tuple[List[str], List[Tuple[str, str]]]:
    """Generate every YAML in `folder`. Returns (generated, errors)."""
    yaml_files = discover_yaml_files(folder)
    if not yaml_files:
        print(f"No YAML files found in: {folder}")
        return [], []

    generated: List[str] = []
    errors: List[Tuple[str, str]] = []

    for yaml_file in yaml_files:
        try:
            module_name = generate_one(
                yaml_file,
                templates_dir=templates_dir,
                src_dir=src_dir,
                app_module_path=app_module_path,   # <-- ADD THIS
                project_root=project_root,
                dry_run=dry_run,
                force=force,
            )
            generated.append(module_name)
        except Exception as exc:  # collect and continue (unless fail-fast)
            errors.append((yaml_file.name, str(exc)))
            if fail_fast:
                break

    return generated, errors

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Generate NestJS clean-architecture modules from YAML. "
            "Pass a single YAML file, or a folder of YAML files for bulk."
        ),
    )
    parser.add_argument(
        "config",
        type=Path,
        help="Path to a module YAML file, or a folder of YAML files.",
    )
    parser.add_argument(
        "--templates",
        type=Path,
        default=Path("templates"),
        help="Directory containing the .tpl template files.",
    )
    parser.add_argument(
        "--src",
        type=Path,
        default=Path("src"),
        help="Root source directory where modules are generated.",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Project root where .generator.manifest.json is stored.",
    )
    parser.add_argument(
        "--app-module",
        type=Path,
        default=None,
        help=(
            "Path to app.module.ts for auto-registration. "
            "Defaults to <src>/app.module.ts."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and render without writing files or the manifest.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing generated files.",
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="During bulk generation, stop at the first error.",
    )
    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    target: Path = args.config
    if not target.exists():
        print(f"ERROR: config path does not exist: {target}")
        sys.exit(1)


    # Default app.module.ts to <src>/app.module.ts when not provided
    app_module_path = args.app_module or (args.src / "app.module.ts")

    common: Dict[str, Path | bool] = dict(
        templates_dir=args.templates,
        src_dir=args.src,
        app_module_path=app_module_path,   
        project_root=args.project_root,
        dry_run=args.dry_run,
        force=args.force,
    )
    # ---- Bulk: target is a folder ------------------------------------
    if target.is_dir():
        generated, errors = generate_bulk(target, fail_fast=args.fail_fast, **common)

        print("\n" + "=" * 60)
        print("Bulk generation summary")
        print("=" * 60)
        print(f"Generated: {len(generated)}")
        for name in generated:
            print(f"  [ok] {name}")
        if errors:
            print(f"Failed:    {len(errors)}")
            for name, message in errors:
                print(f"  [err] {name}: {message}")
            sys.exit(1)
        return

    # ---- Single: target is a file ------------------------------------
    try:
        module_name = generate_one(target, **common)
        print(f"\nGenerated module: {module_name}")
    except Exception as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()