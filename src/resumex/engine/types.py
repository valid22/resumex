from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class ThemeCompiler:
    engine: str  # pdflatex, xelatex, lualatex
    latexmk: bool = True


@dataclass(frozen=True)
class Theme:
    id: str
    allowed_sections: List[str]
    section_templates: Dict[str, str]
    section_models: Dict[str, str]  # "module:Attr"
    compiler: ThemeCompiler
    options: Dict[str, Any]
    # filesystem roots (resolved at runtime)
    theme_root: Path


@dataclass(frozen=True)
class BuildResult:
    pdf_path: Path
    tex_path: Optional[Path]
