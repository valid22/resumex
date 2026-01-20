from resumex.engine.loader import load_theme
from resumex.engine.renderer import render_main, escape_tex

def test_escape_tex():
    assert escape_tex("Hello & World") == r"Hello \& World"
    assert escape_tex("Price $100") == r"Price \$100"
    assert escape_tex("Under_score") == r"Under\_score"
    assert escape_tex(None) == ""

def test_render_custom_theme():
    # Use our test theme
    import os
    from pathlib import Path
    theme_path = str(Path("tests/themes/test-theme").resolve())
    theme = load_theme(theme_path)
    
    sections = {
        "header": {
            "name": "Test User",
            "contacts": [{"text": "test@example.com"}]
        },
        "summary": {
            "text": "This is a & test summary."
        }
    }
    
    # We need to pass validated Pydantic models to render_main if we want to mimic pipeline
    # or just raw dicts if Jinja handles it (renderer.py says Jinja handles it)
    # But validator.py returns dict[str, BaseModel]
    from resumex.engine.validator import validate_resume
    _, validated = validate_resume({"sections": sections}, theme)
    
    output = render_main(theme, validated)
    
    assert r"\section{ Test User }" in output
    assert "test@example.com" in output
    assert "Summary" in output
    assert r"This is a \& test summary." in output
