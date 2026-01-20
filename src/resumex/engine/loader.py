from __future__ import annotations

import importlib
import yaml
from pathlib import Path
from typing import Any, Dict

from .types import Theme, ThemeCompiler
from ..themes.registry import resolve_theme_path


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Top-level YAML must be a mapping/object.")
    return data


def load_theme(theme_id: str) -> Theme:
    theme_root = resolve_theme_path(theme_id)
    theme_yaml = theme_root / "theme.yaml"
    if not theme_yaml.exists():
        raise FileNotFoundError(f"Theme '{theme_id}' missing theme.yaml at {theme_yaml}")

    raw: Dict[str, Any] = yaml.safe_load(theme_yaml.read_text(encoding="utf-8")) or {}
    
    # Only enforce ID mismatch check for bundled themes (which typically don't have slashes in their ID)
    if "/" not in theme_id and "\\" not in theme_id:
        if raw.get("id") != theme_id:
            raise ValueError(f"Theme id mismatch: expected '{theme_id}' but theme.yaml defines id='{raw.get('id')}'")

    compiler_raw = raw.get("compiler") or {}
    compiler = ThemeCompiler(
        engine=str(compiler_raw.get("engine", "pdflatex")),
        latexmk=bool(compiler_raw.get("latexmk", True)),
    )

    allowed_sections = list(raw.get("allowed_sections") or [])
    section_templates = dict(raw.get("section_templates") or {})
    section_models = dict(raw.get("section_models") or {})
    options = dict(raw.get("options") or {})

    # Basic integrity checks
    for sec in allowed_sections:
        if sec not in section_templates:
            raise ValueError(f"Theme '{theme_id}': allowed section '{sec}' missing template mapping.")
        if sec not in section_models:
            raise ValueError(f"Theme '{theme_id}': allowed section '{sec}' missing model mapping.")

    return Theme(
        id=raw.get("id") or theme_id,
        allowed_sections=allowed_sections,
        section_templates=section_templates,
        section_models=section_models,
        compiler=compiler,
        options=options,
        theme_root=theme_root,
    )


def import_symbol(path: str):
    """Import a symbol from 'module:Attr'"""
    if ":" not in path:
        raise ValueError(f"Invalid import path '{path}'. Expected 'module:Attr'.")
    mod, attr = path.split(":", 1)
    m = importlib.import_module(mod)
    try:
        return getattr(m, attr)
    except AttributeError as e:
        raise ImportError(f"Module '{mod}' has no attribute '{attr}'") from e
