from pathlib import Path


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_text_file(
    *,
    root: Path,
    relative_path: str,
    content: str,
    force: bool = False,
    dry_run: bool = False,
) -> None:
    destination = root / relative_path

    if dry_run:
        print(f"[dry-run] {destination}")
        return

    ensure_directory(destination.parent)

    if destination.exists() and not force:
        print(f"[skipped] {destination}")
        return

    destination.write_text(
        content.lstrip("\n"),
        encoding="utf-8",
    )

    print(f"[created] {destination}")