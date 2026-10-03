from pathlib import Path
from string import Template
from typing import Any, Dict


def load_template(
    templates_dir: Path,
    template_path: str,
) -> str:
    path = templates_dir / template_path

    if not path.exists():
        raise FileNotFoundError(f"Template not found: {path}")

    return path.read_text(encoding="utf-8")


def render_template(
    template_content: str,
    context: Dict[str, Any],
) -> str:
    return Template(template_content).safe_substitute(context)
