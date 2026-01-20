from __future__ import annotations

import typer
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

from .engine.pipeline import build_pdf, render_tex

app = typer.Typer(add_completion=False)
console = Console()


@app.command()
def build(
    yaml_path: Path = typer.Argument(..., exists=True, dir_okay=False, help="Path to resume YAML."),
    theme: str | None = typer.Option(None, "--theme", help="Theme id (overrides meta.theme)."),
    out: Path = typer.Option(Path("build"), "--out", help="Output directory."),
    keep_tex: bool = typer.Option(False, "--keep-tex", help="Keep generated .tex file."),
    keep_logs: bool = typer.Option(False, "--keep-logs", help="Keep LaTeX build artifacts (.log, .aux, etc.)."),
):
    """Render YAML -> TeX -> PDF."""
    result = build_pdf(
        yaml_path=yaml_path,
        theme_id=theme,
        out_dir=out,
        keep_tex=keep_tex,
        keep_logs=keep_logs,
    )
    console.print(Panel.fit(
        f"PDF: {result.pdf_path}\nTEX: {result.tex_path if result.tex_path else '(deleted)'}",
        title="Build complete"
    ))


@app.command()
def tex(
    yaml_path: Path = typer.Argument(..., exists=True, dir_okay=False, help="Path to resume YAML."),
    theme: str | None = typer.Option(None, "--theme", help="Theme id (overrides meta.theme)."),
    out: Path = typer.Option(Path("build"), "--out", help="Output directory."),
):
    """Render YAML -> TeX only."""
    tex_path = render_tex(yaml_path=yaml_path, theme_id=theme, out_dir=out)
    console.print(Panel.fit(str(tex_path), title="TeX generated"))


if __name__ == "__main__":
    app()
