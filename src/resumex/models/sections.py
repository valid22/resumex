from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class Contact(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str
    href: Optional[str] = None


class HeaderSection(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    contacts: List[Contact] = Field(default_factory=list)


class EducationItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    school: str
    location: str
    degree: str
    dates: str
    details: List[str] = Field(default_factory=list)

    @property
    def details_tex(self) -> str:
        # join with LaTeX line breaks (mirrors your original formatting)
        return " \\ ".join(self.details)


class EducationSection(BaseModel):
    model_config = ConfigDict(extra="forbid")
    items: List[EducationItem]


class ExperienceItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    role: str
    dates: str
    company: str
    location: str
    highlights: List[str] = Field(default_factory=list)


class ExperienceSection(BaseModel):
    model_config = ConfigDict(extra="forbid")
    items: List[ExperienceItem]


class ProjectItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str
    stack: str
    dates: str
    highlights: List[str] = Field(default_factory=list)


class ProjectsSection(BaseModel):
    model_config = ConfigDict(extra="forbid")
    items: List[ProjectItem]


class LeadershipItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str
    org: str
    dates: str
    highlights: List[str] = Field(default_factory=list)


class LeadershipSection(BaseModel):
    model_config = ConfigDict(extra="forbid")
    items: List[LeadershipItem]


class SummarySection(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str


class HonorsItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str
    org: str
    dates: str


class HonorsSection(BaseModel):
    model_config = ConfigDict(extra="forbid")
    items: List[HonorsItem]


class SkillsSection(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: str = "Languages & Tools"
    value: str
