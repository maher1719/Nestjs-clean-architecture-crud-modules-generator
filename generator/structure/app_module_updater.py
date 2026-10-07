"""Idempotent registration of generated modules into app.module.ts.

Before adding an import or an entry in the @Module imports array, we check
whether the module is already present, so repeated runs (including --force)
never create duplicates.
"""
from __future__ import annotations

import os
import re
from pathlib import Path


IMPORTS_MARKER = "// imports generated"
MODULES_MARKER = "// Modules generated"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _line_indent(content: str, marker: str) -> str:
    """Return the leading whitespace of the line containing `marker`."""
    idx = content.find(marker)
    if idx == -1:
        return ""
    line_start = content.rfind("\n", 0, idx) + 1
    segment = content[line_start:idx]
    return segment[: len(segment) - len(segment.lstrip(" \t"))]


def _relative_import_path(app_module_path: Path, module_file_path: Path) -> str:
    """Compute the TS import path from app.module.ts to the module file."""
    app_dir = app_module_path.resolve().parent
    target = module_file_path.resolve().with_suffix("")  # strip .ts
    rel = os.path.relpath(target, app_dir).replace(os.sep, "/")
    if not rel.startswith("."):
        rel = "./" + rel
    return rel


def _has_import(content: str, class_name: str) -> bool:
    """True if an *active* (non-commented) import of class_name exists."""
    pattern = re.compile(
        r"^[ \t]*import\s*\{[^}]*\b" + re.escape(class_name) + r"\b[^}]*\}\s*from",
        re.MULTILINE,
    )
    return bool(pattern.search(content))


def _has_registration(content: str, class_name: str) -> bool:
    """True if class_name already appears in the @Module imports array."""
    match = re.search(r"imports\s*:\s*\[", content)
    if not match:
        return False

    start = match.end()
    marker_idx = content.find(MODULES_MARKER, start)
    end = marker_idx if marker_idx != -1 else len(content)
    region = content[start:end]

    # Ignore commented-out lines so a "// FooModule," doesn't block us.
    active_lines = [
        line for line in region.split("\n")
        if not line.strip().startswith("//")
    ]
    active_region = "\n".join(active_lines)

    return bool(re.search(r"\b" + re.escape(class_name) + r"\b", active_region))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def register_module(
    app_module_path: Path,
    module_class_name: str,
    module_file_path: Path,
    *,
    dry_run: bool = False,
) -> bool:
    """Register a module in app.module.ts. Returns True if anything changed."""
    path = Path(app_module_path)
    if not path.exists():
        raise FileNotFoundError(f"app.module.ts not found: {path}")

    import_path = _relative_import_path(path, Path(module_file_path))

    content = path.read_text(encoding="utf-8")
    original = content
    added_import = False
    added_registration = False

    # 1. Import statement (skip if already present)
    if not _has_import(content, module_class_name):
        indent = _line_indent(content, IMPORTS_MARKER)
        import_line = f"{indent}import {{ {module_class_name} }} from '{import_path}';"
        if IMPORTS_MARKER in content:
            content = content.replace(
                IMPORTS_MARKER, import_line + "\n" + IMPORTS_MARKER, 1
            )
        else:
            content = content.replace("@Module(", import_line + "\n@Module(", 1)
        added_import = True

    # 2. imports[] registration (skip if already present)
    if not _has_registration(content, module_class_name):
        indent = _line_indent(content, MODULES_MARKER)
        registration_line = f"{indent}{module_class_name},"
        if MODULES_MARKER not in content:
            raise ValueError(
                f"Could not find '{MODULES_MARKER}' marker in {path}. "
                "Add it inside the @Module imports array."
            )
        content = content.replace(
            MODULES_MARKER, registration_line + "\n" + MODULES_MARKER, 1
        )
        added_registration = True

    changed = content != original

    if changed and not dry_run:
        path.write_text(content, encoding="utf-8")

    if added_import or added_registration:
        action = "[dry-run] would register" if dry_run else "[registered]"
        print(f"{action} {module_class_name} in {path.name}")
    else:
        print(f"[skipped] {module_class_name} already registered in {path.name}")

    return changed