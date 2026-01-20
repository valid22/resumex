import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from resumex.engine.compiler import compile_pdf, LatexCompileError
from resumex.engine.types import Theme, ThemeCompiler

@patch("subprocess.run")
@patch("shutil.which")
def test_compile_pdf_latexmk(mock_which, mock_run, tmp_path):
    mock_which.side_effect = lambda x: f"/usr/bin/{x}"
    mock_run.return_value = MagicMock(returncode=0)
    
    out_dir = (tmp_path / "build").resolve()
    theme = Theme(
        id="test",
        allowed_sections=[],
        section_templates={},
        section_models={},
        compiler=ThemeCompiler(engine="pdflatex", latexmk=True),
        options={},
        theme_root=tmp_path / "theme"
    )
    
    tex_path = tmp_path / "resume.tex"
    
    # Mock pdf existence
    with patch("pathlib.Path.exists", return_value=True):
        pdf_path = compile_pdf(theme, tex_path, out_dir)
    
    assert pdf_path.resolve() == (out_dir / "resume.pdf").resolve()
    # Verify latexmk was called
    args = mock_run.call_args[0][0]
    assert "/usr/bin/latexmk" in args
    assert "-pdf" in args
    assert "-pdflatex" in args

@patch("subprocess.run")
@patch("shutil.which")
def test_compile_pdf_direct_engine(mock_which, mock_run, tmp_path):
    # Mock latexmk as missing, but pdflatex as present
    mock_which.side_effect = lambda x: "/usr/bin/pdflatex" if x == "pdflatex" else None
    mock_run.return_value = MagicMock(returncode=0)
    
    out_dir = (tmp_path / "build").resolve()
    theme = Theme(
        id="test",
        allowed_sections=[],
        section_templates={},
        section_models={},
        compiler=ThemeCompiler(engine="pdflatex", latexmk=True),
        options={},
        theme_root=tmp_path / "theme"
    )
    
    tex_path = tmp_path / "resume.tex"
    
    with patch("pathlib.Path.exists", return_value=True):
        pdf_path = compile_pdf(theme, tex_path, out_dir)
    
    assert pdf_path.resolve() == (out_dir / "resume.pdf").resolve()
    # Verify pdflatex was called (twice is the fallback behavior)
    assert mock_run.call_count == 2
    args = mock_run.call_args[0][0]
    assert "/usr/bin/pdflatex" in args

def test_compile_pdf_failure(tmp_path):
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=1, stdout="error", stderr="very bad")
        
        theme = Theme(
            id="test",
            allowed_sections=[],
            section_templates={},
            section_models={},
            compiler=ThemeCompiler(engine="pdflatex", latexmk=False),
            options={},
            theme_root=tmp_path / "theme"
        )
        
        with pytest.raises(LatexCompileError):
            compile_pdf(theme, tmp_path / "resume.tex", tmp_path / "build")
