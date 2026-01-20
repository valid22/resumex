import pytest
from pathlib import Path
from resumex.engine.loader import load_theme, resolve_theme_path

def test_resolve_bundled_theme():
    path = resolve_theme_path("default")
    assert path.exists()
    assert (path / "theme.yaml").exists()

def test_resolve_custom_theme():
    custom_path = Path("tests/themes/test-theme").resolve()
    path = resolve_theme_path(str(custom_path))
    assert path == custom_path

def test_resolve_nonexistent_theme():
    with pytest.raises(FileNotFoundError):
        resolve_theme_path("nonexistent-theme-12345")

def test_load_bundled_theme():
    theme = load_theme("default")
    assert theme.id == "default"
    assert "header" in theme.allowed_sections

def test_load_custom_theme():
    custom_path = str(Path("tests/themes/test-theme").resolve())
    theme = load_theme(custom_path)
    # The ID in theme.yaml is test-theme
    assert theme.id == "test-theme"
    assert "header" in theme.allowed_sections
