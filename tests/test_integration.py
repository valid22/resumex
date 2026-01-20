import pytest
from pathlib import Path
from resumex.engine.pipeline import build_pdf, render_tex

def test_integration_custom_theme(tmp_path):
    # Setup YAML
    yaml_path = tmp_path / "resume.yaml"
    yaml_path.write_text("""
sections:
  header:
    name: Integration Test
    contacts: [{"text": "int@example.com"}]
  summary:
    text: Integration summary.
""")
    
    # Use the test theme we created
    custom_theme_path = str(Path("tests/themes/test-theme").resolve())
    
    # Test render_tex (no LaTeX needed)
    out_dir = tmp_path / "build"
    tex_path = render_tex(yaml_path, custom_theme_path, out_dir)
    
    assert tex_path.exists()
    content = tex_path.read_text()
    assert "Integration Test" in content
    assert "int@example.com" in content
    assert "Integration summary" in content
