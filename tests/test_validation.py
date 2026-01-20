from pathlib import Path
import yaml
import pytest

from resumex.engine.loader import load_theme
from resumex.engine.validator import validate_resume


from resumex.engine.loader import load_theme
from resumex.engine.validator import validate_resume
from resumex.models.sections import HeaderSection, SummarySection

def test_unknown_section_rejected():
    theme = load_theme("default")
    data = {
        "meta": {"theme": "default"},
        "sections": {
            "header": {"name": "X", "contacts": []},
            "unknown": {"foo": "bar"},
        },
    }
    with pytest.raises(ValueError, match="Unknown section"):
        validate_resume(data, theme)

def test_valid_minimal_resume():
    theme = load_theme("default")
    data = {
        "sections": {
            "header": {"name": "Jane Doe", "contacts": [{"text": "jane@example.com"}]}
        }
    }
    envelope, validated = validate_resume(data, theme)
    assert envelope.sections["header"]["name"] == "Jane Doe"
    assert isinstance(validated["header"], HeaderSection)
    assert validated["header"].name == "Jane Doe"

def test_invalid_section_data():
    theme = load_theme("default")
    data = {
        "sections": {
            "header": {"name": 123, "contacts": "not-a-list"}
        }
    }
    with pytest.raises(Exception): # Pydantic ValidationError
        validate_resume(data, theme)

def test_summary_section():
    theme = load_theme("default")
    data = {
        "sections": {
            "header": {"name": "X", "contacts": []},
            "summary": {"text": "My summary"}
        }
    }
    envelope, validated = validate_resume(data, theme)
    assert isinstance(validated["summary"], SummarySection)
    assert validated["summary"].text == "My summary"
