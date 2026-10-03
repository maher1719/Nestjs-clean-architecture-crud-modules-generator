import os
from pathlib import Path


def update_app_module(
    app_module_path: Path,
    module_file_path: Path,
    module_class_name: str,
    module_name: str,
    dry_run: bool = False,
) -> None:
    if not app_module_path.exists():
        print(f"[skipped] {app_module_path} not found. Cannot register module.")
        return

    content = app_module_path.read_text(encoding="utf-8")

    # Calculate relative import path safely (e.g. './employees/employees.module')
    rel_path = os.path.relpath(module_file_path, app_module_path.parent)
    import_path_str = "./" + rel_path.replace("\\", "/").replace(".ts", "")

    import_statement = f"import {{ {module_class_name} }} from '{import_path_str}';"
    module_import_entry = f"    {module_class_name},"

    # Check if already imported to prevent duplicates
    if import_statement in content:
        print(f"[skipped] {module_class_name} is already imported in {app_module_path}")
        return

    modified = False

    # 1. Insert import statement above the marker
    import_marker = "// imports generated"
    if import_marker in content:
        content = content.replace(
            import_marker,
            f"{import_statement}\n{import_marker}"
        )
        modified = True
    else:
        print(f"[warning] Marker '{import_marker}' not found in {app_module_path}")

    # 2. Insert module into imports array above the marker
    module_marker = "// Modules generated"
    if module_marker in content:
        content = content.replace(
            module_marker,
            f"{module_import_entry}\n{module_marker}"
        )
        modified = True
    else:
        print(f"[warning] Marker '{module_marker}' not found in {app_module_path}")

    if not modified:
        return

    if dry_run:
        print(f"[dry-run] Would update {app_module_path}")
        print(f"  + {import_statement}")
        print(f"  + {module_import_entry.strip()}")
        return

    app_module_path.write_text(content, encoding="utf-8")
    print(f"[updated] Registered {module_class_name} in {app_module_path}")
