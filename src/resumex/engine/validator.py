from __future__ import annotations

from typing import Any, Dict

from pydantic import BaseModel

from .types import Theme
from .loader import import_symbol
from ..models.envelope import ResumeEnvelope


def validate_resume(envelope_data: dict[str, Any], theme: Theme) -> tuple[ResumeEnvelope, dict[str, BaseModel]]:
    envelope = ResumeEnvelope.model_validate(envelope_data)

    yaml_sections = set(envelope.sections.keys())
    allowed = set(theme.allowed_sections)
    unknown = yaml_sections - allowed
    if unknown:
        raise ValueError(
            f"Unknown section(s) for theme '{theme.id}': {sorted(unknown)}. Allowed: {theme.allowed_sections}"
        )

    validated: dict[str, BaseModel] = {}
    for sec_id, payload in envelope.sections.items():
        model_cls = import_symbol(theme.section_models[sec_id])
        validated[sec_id] = model_cls.model_validate(payload)

    return envelope, validated
