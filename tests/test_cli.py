from typer.testing import CliRunner
from resumex.cli import app
from pathlib import Path
import pytest
import shutil

runner = CliRunner()

def test_cli_tex_command(tmp_path):
    yaml_path = tmp_path / "resume.yaml"
    yaml_path.write_text("""
sections:
  header:
    name: CLI Test
    contacts: []
""")
    
    out_dir = tmp_path / "out"
    result = runner.invoke(app, ["tex", str(yaml_path), "--out", str(out_dir)])
    
    assert result.exit_code == 0
    assert (out_dir / "resume.tex").exists()
    assert "CLI Test" in (out_dir / "resume.tex").read_text()

def test_cli_build_command_mocked(tmp_path, monkeypatch):
    yaml_path = tmp_path / "resume.yaml"
    yaml_path.write_text("""
sections:
  header:
    name: Build Test
    contacts: []
""")
    
    # Mock the pipeline functions to avoid actual LaTeX requirement
    def mock_build_pdf(*args, **kwargs):
        from resumex.engine.types import BuildResult
        pdf = tmp_path / "out" / "resume.pdf"
        pdf.parent.mkdir(parents=True, exist_ok=True)
        pdf.touch()
        return BuildResult(pdf_path=pdf, tex_path=None)
    
    import resumex.cli
    monkeypatch.setattr("resumex.cli.build_pdf", mock_build_pdf)
    
    out_dir = tmp_path / "out"
    result = runner.invoke(app, ["build", str(yaml_path), "--out", str(out_dir)])
    
    assert result.exit_code == 0
    assert (out_dir / "resume.pdf").exists()
    assert "Build complete" in result.stdout

def test_cli_invalid_yaml():
    result = runner.invoke(app, ["tex", "nonexistent.yaml"])
    assert result.exit_code != 0
