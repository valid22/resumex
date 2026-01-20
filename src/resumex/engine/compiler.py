from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Optional

from .types import Theme


class LatexCompileError(RuntimeError):
    pass


def _run(cmd: list[str], cwd: Path) -> None:
    p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    if p.returncode != 0:
        raise LatexCompileError(
            "LaTeX compilation failed.\n"
            f"Command: {' '.join(cmd)}\n\nSTDOUT:\n{p.stdout}\n\nSTDERR:\n{p.stderr}"
        )


def compile_pdf(theme: Theme, tex_path: Path, out_dir: Path, keep_logs: bool = False) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    tex_path = tex_path.resolve()
    out_dir = out_dir.resolve()

    engine = theme.compiler.engine
    pdf_name = tex_path.with_suffix(".pdf").name
    pdf_path = out_dir / pdf_name

    latexmk = shutil.which("latexmk")
    if theme.compiler.latexmk and latexmk:
        # latexmk writes output in cwd; use -outdir for cleanliness
        cmd = [
            latexmk,
            "-pdf",
            f"-{engine}",
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-outdir={str(out_dir)}",
            str(tex_path),
        ]
        _run(cmd, cwd=out_dir)
    else:
        eng = shutil.which(engine)
        if not eng:
            raise LatexCompileError(
                f"Neither latexmk nor the engine '{engine}' is available on PATH. Install a LaTeX distribution."
            )
        # Run twice for references stability (minimal)
        cmd = [eng, "-interaction=nonstopmode", "-halt-on-error", f"-output-directory={str(out_dir)}", str(tex_path)]
        _run(cmd, cwd=out_dir)
        _run(cmd, cwd=out_dir)

    if not pdf_path.exists():
        raise LatexCompileError(f"Expected PDF not found at {pdf_path}")

    if not keep_logs:
        for ext in ["aux", "log", "out", "fls", "fdb_latexmk", "toc"]:
            p = (out_dir / tex_path.with_suffix(f".{ext}").name)
            if p.exists():
                p.unlink(missing_ok=True)

    return pdf_path
