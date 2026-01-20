from __future__ import annotations

from pathlib import Path
import importlib.resources as ir


def resolve_theme_path(theme_id: str) -> Path:
    """Resolve an installed theme folder path or a direct filesystem path."""
    # 1. Try as a direct path first (for custom themes)
    path = Path(theme_id)
    if path.is_dir() and (path / "theme.yaml").exists():
        return path.resolve()

    # 2. Fallback to bundled themes
    base = ir.files("resumex") / "themes_data"
    theme_dir = base / theme_id
    # Convert Traversable to actual filesystem path
    with ir.as_file(theme_dir) as p:
        if not p.exists():
            raise FileNotFoundError(
                f"Theme '{theme_id}' not found. "
                f"It is neither a local directory with theme.yaml nor a bundled theme."
            )
        return p
