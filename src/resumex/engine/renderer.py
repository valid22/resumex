from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
import re

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

from .types import Theme


_LATEX_SPECIALS = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}

_LATEX_SPECIALS_RE = re.compile(r"(\\|[&%$#_{}~^])")


def escape_tex(value: Any) -> str:
    if value is None:
        return ""
    s = str(value)
    return _LATEX_SPECIALS_RE.sub(lambda m: _LATEX_SPECIALS[m.group(0)], s)


def make_env(theme: Theme) -> Environment:
    loader = FileSystemLoader([str(theme.theme_root / "templates"), str(theme.theme_root)])
    env = Environment(
        loader=loader,
        undefined=StrictUndefined,
        autoescape=False,  # LaTeX is not HTML; we control escaping via filter.
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["escape_tex"] = escape_tex
    return env


def render_main(theme: Theme, sections: Dict[str, Any]) -> str:
    env = make_env(theme)
    template = env.get_template("templates/main.tex.j2")
    return template.render(theme=theme, sections=sections)
