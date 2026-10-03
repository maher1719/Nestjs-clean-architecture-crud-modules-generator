from argparse import ArgumentParser
from pathlib import Path

from .config_loader import load_config
from .generator import generate_module


def main() -> None:
    parser = ArgumentParser(
        description=(
            "Generate a NestJS Clean Architecture CRUD module "
            "from a YAML definition."
        )
    )

    parser.add_argument(
        "config",
        type=Path,
        help="Path to the module YAML file. Example: organization.yml",
    )

    parser.add_argument(
        "--templates",
        type=Path,
        default=Path("templates"),
        help="Path to template directory. Default: ./templates",
    )

    parser.add_argument(
        "--src",
        type=Path,
        default=Path("src"),
        help="NestJS source directory. Default: ./src",
    )
    parser.add_argument(
        "--app-module",
        type=Path,
        default=Path("src/app.module.ts"),
        help="Path to the main app.module.ts file. Default: src/app.module.ts",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and render the module without writing files.",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing generated files.",
    )

    args = parser.parse_args()

    try:
        config = load_config(args.config)

        generate_module(
            config,
            templates_dir=args.templates,
            src_dir=args.src,
            app_module_path=args.app_module,
            dry_run=args.dry_run,
            force=args.force,
        )

    except Exception as exc:
        print(f"ERROR: {exc}")
        raise SystemExit(1)
