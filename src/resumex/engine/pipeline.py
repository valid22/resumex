from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from .loader import load_yaml, load_theme
from .validator import validate_resume
from .renderer import render_main
from .compiler import compile_pdf
from .types import BuildResult


def render_tex(yaml_path: Path, theme_id: str | None, out_dir: Path) -> Path:
    data = load_yaml(yaml_path)
    meta = (data.get("meta") or {})
    theme_name = theme_id or meta.get("theme") or "default"
    theme = load_theme(theme_name)

    _envelope, validated_sections = validate_resume(data, theme)

    # Convert validated pydantic models to plain dicts for templates, preserving computed properties
    # We pass the actual models, but Jinja handles attribute access well. Keep models for convenience.
    tex = render_main(theme=theme, sections=validated_sections)

    out_dir.mkdir(parents=True, exist_ok=True)
    tex_path = out_dir / (yaml_path.stem + ".tex")
    tex_path.write_text(tex, encoding="utf-8")
    return tex_path


def build_pdf(
    yaml_path: Path,
    theme_id: str | None,
    out_dir: Path,
    keep_tex: bool = False,
    keep_logs: bool = False,
) -> BuildResult:
    tex_path = render_tex(yaml_path=yaml_path, theme_id=theme_id, out_dir=out_dir)
    theme_name = theme_id or (load_yaml(yaml_path).get("meta") or {}).get("theme") or "default"
    theme = load_theme(theme_name)

    pdf_path = compile_pdf(theme=theme, tex_path=tex_path, out_dir=out_dir, keep_logs=keep_logs)

    final_tex_path = tex_path if keep_tex else None
    if not keep_tex:
        tex_path.unlink(missing_ok=True)

    return BuildResult(pdf_path=pdf_path, tex_path=final_tex_path)
