from argparse import ArgumentParser
from pathlib import Path

from .templates_writer import write_all_templates


def main() -> None:
    parser = ArgumentParser(
        description=(
            "Generate NestJS Clean Architecture template files "
            "used by create_structure.py."
        )
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("templates"),
        help="Output directory for template files. Default: ./templates",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing template files.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print files that would be written without writing them.",
    )

    args = parser.parse_args()

    write_all_templates(
        output_dir=args.output,
        force=args.force,
        dry_run=args.dry_run,
    )