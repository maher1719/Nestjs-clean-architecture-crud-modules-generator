"""Manifest bookkeeping for generated modules.

Maintains a `.generator.manifest.json` at the project root recording every
module the generator has produced, so modules can be retrieved, validated,
and reconciled later.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


MANIFEST_FILENAME = ".generator.manifest.json"
SCHEMA_VERSION = 1
GENERATOR_VERSION = "v2"


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

def manifest_path(project_root: Path) -> Path:
    return Path(project_root) / MANIFEST_FILENAME


def _relative_to_root(path: Path, project_root: Path) -> str:
    """Return `path` relative to `project_root` when possible (portable)."""
    try:
        return str(Path(path).resolve().relative_to(Path(project_root).resolve()))
    except ValueError:
        return str(Path(path).resolve())


# ---------------------------------------------------------------------------
# Load / write
# ---------------------------------------------------------------------------

def _empty_manifest() -> Dict[str, Any]:
    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatorVersion": GENERATOR_VERSION,
        "modules": {},
    }


def load_manifest(project_root: Path) -> Dict[str, Any]:
    path = manifest_path(project_root)
    if not path.exists():
        return _empty_manifest()
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (json.JSONDecodeError, OSError):
        return _empty_manifest()
    if not isinstance(data, dict) or not isinstance(data.get("modules"), dict):
        return _empty_manifest()
    return data


def _write_manifest(project_root: Path, manifest: Dict[str, Any]) -> None:
    path = manifest_path(project_root)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


# ---------------------------------------------------------------------------
# Entry building
# ---------------------------------------------------------------------------

def build_module_entry(
    config: Dict[str, Any],
    config_path: Path,
    output_path: Path,
    project_root: Path,
) -> Dict[str, Any]:
    entity = config.get("entity", {})
    module_name = config.get("module", "")
    relations = config.get("relations") or []

    relation_summaries: List[Dict[str, Any]] = []
    for relation in relations:
        if not isinstance(relation, dict):
            continue
        relation_summaries.append({
            "type": relation.get("type"),
            "target": relation.get("target"),
            "targetModule": relation.get("targetModule"),
        })

    return {
        "entity": entity.get("name"),
        "table": entity.get("table"),
        "configPath": _relative_to_root(config_path, project_root),
        "outputPath": _relative_to_root(output_path, project_root),
        "moduleFile": _relative_to_root(
            Path(output_path) / f"{module_name}.module.ts",
            project_root,
        ),
        "parent": config.get("parent"),
        "relations": relation_summaries,
        "operations": config.get("operations", []),
        "generatedAt": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Upsert
# ---------------------------------------------------------------------------

def upsert_module(
    project_root: Path,
    module_name: str,
    entry: Dict[str, Any],
) -> Path:
    """Insert or update a module entry, then persist the manifest."""
    manifest = load_manifest(project_root)
    manifest["schemaVersion"] = SCHEMA_VERSION
    manifest["generatorVersion"] = GENERATOR_VERSION
    manifest.setdefault("modules", {})[module_name] = entry
    _write_manifest(project_root, manifest)
    return manifest_path(project_root)