"""Tests for YAML loader."""

import pytest
from pathlib import Path
import yaml

from resumodel.loader import load_shared_data, build_resume_context
from resumodel.models import (
    PersonalInfo,
    SharedData,
    Experience,
    Project,
    Profile,
)


def test_load_shared_data_not_found() -> None:
    """Test loading from non-existent directory."""
    with pytest.raises(FileNotFoundError):
        load_shared_data(Path("/nonexistent/directory"))


def test_load_shared_data_empty_dir(tmp_path: Path) -> None:
    """Test loading from empty directory."""
    shared = load_shared_data(tmp_path)
    assert len(shared.experiences) == 0
    assert len(shared.projects) == 0


def test_load_shared_data_with_files(tmp_path: Path) -> None:
    """Test loading shared data from directory."""
    # Create experiences file
    exp_file = tmp_path / "experiences.yml"
    exp_data = {
        "experiences": {
            "EXP1": {
                "title": "Engineer",
                "company": "TechCo",
                "date": "2020",
                "location": "NYC",
            }
        }
    }
    with open(exp_file, "w") as f:
        yaml.dump(exp_data, f)

    # Create projects file
    proj_file = tmp_path / "projects.yml"
    proj_data = {
        "projects": {
            "PROJ1": {
                "name": "Cool Project",
                "link": "https://github.com/user/proj",
                "description": "A project",
            }
        }
    }
    with open(proj_file, "w") as f:
        yaml.dump(proj_data, f)

    shared = load_shared_data(tmp_path)
    assert "EXP1" in shared.experiences
    assert shared.experiences["EXP1"].title == "Engineer"
    assert "PROJ1" in shared.projects


def test_build_resume_context(tmp_path: Path) -> None:
    """Test building resume context."""
    from pydantic import HttpUrl

    # Create shared data
    shared = SharedData()
    shared.experiences["EXP1"] = Experience(
        title="Developer",
        company="StartupCo",
        date="2023",
    )
    shared.projects["PROJ1"] = Project(
        name="Test Project",
        link=HttpUrl("https://github.com/test"),
        description="Test",
    )
    shared.profiles["TEST"] = Profile(
        title="Software Developer",
        summary="A developer",
        experiences=["EXP1"],
        projects=["PROJ1"],
    )

    # Create personal info
    personal_info = PersonalInfo(name="Test User")

    # Build context with new signature
    context = build_resume_context(personal_info, "TEST", shared)

    # Access as Pydantic model attributes
    assert context.title == "Software Developer"
    assert context.summary == "A developer"
    assert len(context.sections.experiences) == 1
    assert len(context.sections.projects) == 1
    assert context.sections.experiences[0].title == "Developer"


def test_build_resume_context_missing_profile() -> None:
    """Test building context with missing profile."""
    shared = SharedData()
    personal_info = PersonalInfo(name="Test")

    with pytest.raises(ValueError, match="Profile 'MISSING' not found"):
        build_resume_context(personal_info, "MISSING", shared)


def test_build_resume_context_missing_reference() -> None:
    """Test building context with missing experience reference."""
    shared = SharedData()
    shared.profiles["TEST"] = Profile(
        title="Test",
        summary="Test",
        experiences=["MISSING_EXP"],  # This experience doesn't exist
    )

    personal_info = PersonalInfo(name="Test")

    with pytest.raises(KeyError):
        build_resume_context(personal_info, "TEST", shared)
