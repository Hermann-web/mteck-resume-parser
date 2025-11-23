"""Pydantic models for resume components."""

from typing import Literal, Optional
from pydantic import BaseModel, Field, HttpUrl


class PersonalInfo(BaseModel):
    """Personal information for the resume header."""

    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    linkedin: Optional[HttpUrl] = None
    github: Optional[HttpUrl] = None
    blog: Optional[HttpUrl] = None
    projects_page: Optional[HttpUrl] = None
    pypi: Optional[HttpUrl] = None
    passport_dev: Optional[HttpUrl] = None
    location: Optional[str] = None


class SkillCategory(BaseModel):
    """A category of skills with items."""

    category: str
    items: list[str]


class Experience(BaseModel):
    """Work experience entry."""

    title: str
    company: str
    date: str
    location: str = ""
    bullet_points: list[str] = Field(default_factory=list)
    link: Optional[HttpUrl] = None


class Project(BaseModel):
    """Project entry."""

    name: str
    link: Optional[HttpUrl] = None
    description: str


class Education(BaseModel):
    """Education entry."""

    institution: str
    location: str
    degree: str
    notes: Optional[str] = None


class Certification(BaseModel):
    """Certification or award."""

    name: str
    issuer: str
    credential_link: HttpUrl


class ResearchPaper(BaseModel):
    """Research paper or publication."""

    title: str
    authors: str
    status: Literal["Published", "In Preparation", "Submitted", "Preprint"]
    link: Optional[HttpUrl] = None


class ClubActivity(BaseModel):
    """Club or association activity."""

    name: str
    role: str
    date: str
    description: Optional[str] = None
    link: Optional[HttpUrl] = None


class Hobby(BaseModel):
    """Hobby or interest."""

    name: str
    link: Optional[HttpUrl] = None


class Profile(BaseModel):
    """A resume profile configuration."""

    title: str
    summary: str
    skills: Optional[list[SkillCategory]] = None
    experiences: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    research_papers: list[str] = Field(default_factory=list)
    clubs_and_associations: list[str] = Field(default_factory=list)
    hobbies: list[str] = Field(default_factory=list)


class SharedData(BaseModel):
    """Container for shared resume data."""

    experiences: dict[str, Experience] = Field(default_factory=dict)
    projects: dict[str, Project] = Field(default_factory=dict)
    education: dict[str, Education] = Field(default_factory=dict)
    certifications: dict[str, Certification] = Field(default_factory=dict)
    research_papers: dict[str, ResearchPaper] = Field(default_factory=dict)
    clubs_and_associations: dict[str, ClubActivity] = Field(default_factory=dict)
    hobbies: dict[str, Hobby] = Field(default_factory=dict)
    profiles: dict[str, Profile] = Field(default_factory=dict)


class ResumeSections(BaseModel):
    """Resume sections for validation."""

    skills: Optional[list[SkillCategory]] = None
    experiences: list[Experience] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    certifications: list[Certification] = Field(default_factory=list)
    research_papers: list[ResearchPaper] = Field(default_factory=list)
    clubs_and_associations: list[ClubActivity] = Field(default_factory=list)
    hobbies: list[Hobby] = Field(default_factory=list)


class TemplateContext(BaseModel):
    """Schema for validating template context."""

    personal_info: PersonalInfo
    title: str
    summary: str
    sections: ResumeSections
