from __future__ import annotations

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict


class Meta(BaseModel):
    model_config = ConfigDict(extra="forbid")
    theme: str = "default"
    output: Optional[str] = None


class ResumeEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    meta: Meta = Field(default_factory=Meta)
    sections: Dict[str, Any]
