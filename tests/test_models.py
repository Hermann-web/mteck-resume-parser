"""Tests for Pydantic models."""

import pytest
from pydantic import ValidationError, HttpUrl
from resumodel.models import (
    PersonalInfo,
    SkillCategory,
    Experience,
    Project,
    Education,
    Certification,
    ResearchPaper,
    ClubActivity,
    Hobby,
    Profile,
)


def test_personal_info_valid() -> None:
    """Test PersonalInfo with valid data."""

    info = PersonalInfo(
        name="John Doe",
        email="john@example.com",
        phone="+1234567890",
        linkedin=HttpUrl("https://linkedin.com/in/johndoe"),
    )
    assert info.name == "John Doe"
    assert info.email == "john@example.com"


def test_personal_info_minimal() -> None:
    """Test PersonalInfo with only required fields."""
    info = PersonalInfo(name="Jane Doe")
    assert info.name == "Jane Doe"
    assert info.email is None


def test_skill_category() -> None:
    """Test SkillCategory model."""
    category = SkillCategory(
        category="Programming",
        items=["Python", "JavaScript", "Go"],
    )
    assert category.category == "Programming"
    assert len(category.items) == 3


def test_experience_valid() -> None:
    """Test Experience with all fields."""

    exp = Experience(
        title="Software Engineer",
        company="Tech Corp",
        date="Jan 2020 - Dec 2023",
        location="San Francisco, CA",
        bullet_points=["Built APIs", "Led team"],
        link=HttpUrl("https://example.com"),
    )
    assert exp.title == "Software Engineer"
    assert len(exp.bullet_points) == 2


def test_experience_minimal() -> None:
    """Test Experience with required fields only."""
    exp = Experience(
        title="Developer",
        company="StartupCo",
        date="2023",
    )
    assert exp.location == ""
    assert exp.bullet_points == []


def test_project_valid() -> None:
    """Test Project model."""

    project = Project(
        name="Cool Project",
        link=HttpUrl("https://github.com/user/cool-project"),
        description="A cool project that does things",
    )
    assert project.name == "Cool Project"
    assert isinstance(project.link, HttpUrl)


def test_project_invalid_url() -> None:
    """Test Project with invalid URL."""
    with pytest.raises(ValidationError):
        Project(
            name="Bad Project",
            link="not-a-url",  # type: ignore[arg-type]
            description="Broken link",
        )


def test_education() -> None:
    """Test Education model."""
    edu = Education(
        institution="University of Technology",
        location="Boston, MA",
        degree="B.S. Computer Science",
        notes="Graduated with honors",
    )
    assert edu.institution == "University of Technology"
    assert edu.notes == "Graduated with honors"


def test_certification() -> None:
    """Test Certification model."""

    cert = Certification(
        name="AWS Certified Developer",
        issuer="Amazon Web Services",
        credential_link=HttpUrl("https://aws.amazon.com/cert/123"),
    )
    assert cert.name == "AWS Certified Developer"


def test_research_paper() -> None:
    """Test ResearchPaper model."""

    paper = ResearchPaper(
        title="Deep Learning for NLP",
        authors="Smith, J., Doe, J.",
        status="Published",
        link=HttpUrl("https://arxiv.org/abs/1234.5678"),
    )
    assert paper.status == "Published"


def test_research_paper_invalid_status() -> None:
    """Test ResearchPaper with invalid status."""
    with pytest.raises(ValidationError):
        ResearchPaper(
            title="Bad Paper",
            authors="Nobody",
            status="Invalid Status",  # type: ignore
        )


def test_club_activity() -> None:
    """Test ClubActivity model."""
    club = ClubActivity(
        name="Tech Club",
        role="President",
        date="2020-2023",
        description="Led technical workshops",
    )
    assert club.role == "President"


def test_hobby() -> None:
    """Test Hobby model."""

    hobby = Hobby(name="Gaming", link=HttpUrl("https://twitch.tv/gamer"))
    assert hobby.name == "Gaming"


def test_profile() -> None:
    """Test Profile model."""
    profile = Profile(
        title="Software Engineer",
        summary="Experienced developer",
        experiences=["EXP1", "EXP2"],
        projects=["PROJ1"],
    )
    assert len(profile.experiences) == 2
    assert profile.skills is None
