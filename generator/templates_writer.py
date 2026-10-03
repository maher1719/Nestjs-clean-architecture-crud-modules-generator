from pathlib import Path

from .filesystem import write_text_file
from .templates.registry import TEMPLATE_REGISTRY


def write_all_templates(
    *,
    output_dir: Path,
    force: bool = False,
    dry_run: bool = False,
) -> None:
    if dry_run:
        print(f"[dry-run] Writing templates to: {output_dir.resolve()}")
    else:
        print(f"Writing templates to: {output_dir.resolve()}")

    for relative_path, content in sorted(TEMPLATE_REGISTRY.items()):
        write_text_file(
            root=output_dir,
            relative_path=relative_path,
            content=content,
            force=force,
            dry_run=dry_run,
        )

    print("Done.")