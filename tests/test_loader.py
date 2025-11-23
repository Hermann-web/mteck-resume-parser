"""Tests for YAML loader."""

import pytest
from pathlib import Path
import yaml

from resumodel.loader import (
    load_shared_data,
    build_resume_context,
    load_yaml,
    load_personal_info,
)
from resumodel.models import (
    PersonalInfo,
    SharedData,
    Experience,
    Project,
    Profile,
)
from resumodel.exceptions import ConfigError, DataError


def test_load_yaml_success(tmp_path: Path) -> None:
    """Test loading valid YAML file."""
    test_file = tmp_path / "test.yml"
    test_data = {"name": "Test User", "email": "test@example.com"}
    with open(test_file, "w") as f:
        yaml.dump(test_data, f)

    result = load_yaml(test_file, PersonalInfo)
    assert result.name == "Test User"
    assert result.email == "test@example.com"


def test_load_yaml_missing_file() -> None:
    """Test loading from non-existent file."""
    with pytest.raises(ConfigError, match="Config file not found"):
        load_yaml(Path("/nonexistent/file.yml"), PersonalInfo)


def test_load_yaml_invalid_yaml(tmp_path: Path) -> None:
    """Test loading invalid YAML."""
    test_file = tmp_path / "invalid.yml"
    test_file.write_text("invalid: yaml: content: :[")

    with pytest.raises(ConfigError, match="Invalid YAML"):
        load_yaml(test_file, PersonalInfo)


def test_load_yaml_empty_file(tmp_path: Path) -> None:
    """Test loading empty YAML file."""
    test_file = tmp_path / "empty.yml"
    test_file.write_text("")

    with pytest.raises(ConfigError, match="Empty YAML file"):
        load_yaml(test_file, PersonalInfo)


def test_load_yaml_validation_error(tmp_path: Path) -> None:
    """Test loading YAML with invalid data."""
    test_file = tmp_path / "test.yml"
    # PersonalInfo requires a name field, but we're not providing it
    test_data = {"email": "test@example.com"}
    with open(test_file, "w") as f:
        yaml.dump(test_data, f)

    with pytest.raises(DataError, match="Validation failed"):
        load_yaml(test_file, PersonalInfo)


def test_load_personal_info_success(tmp_path: Path) -> None:
    """Test loading personal info successfully."""
    personal_info_file = tmp_path / "personal_info.yml"
    data = {
        "personal_info": {
            "name": "John Doe",
            "email": "john@example.com",
            "location": "NYC",
        }
    }
    with open(personal_info_file, "w") as f:
        yaml.dump(data, f)

    result = load_personal_info(tmp_path)
    assert result.name == "John Doe"
    assert result.email == "john@example.com"
    assert result.location == "NYC"


def test_load_personal_info_missing_file() -> None:
    """Test loading personal info from non-existent directory."""
    with pytest.raises(ConfigError, match="Personal info file not found"):
        load_personal_info(Path("/nonexistent"))


def test_load_personal_info_invalid_yaml(tmp_path: Path) -> None:
    """Test loading personal info with invalid YAML."""
    personal_info_file = tmp_path / "personal_info.yml"
    personal_info_file.write_text("invalid: yaml: :[")

    with pytest.raises(ConfigError, match="Invalid YAML"):
        load_personal_info(tmp_path)


def test_load_personal_info_missing_key(tmp_path: Path) -> None:
    """Test loading personal info without 'personal_info' key."""
    personal_info_file = tmp_path / "personal_info.yml"
    data = {"wrong_key": {"name": "Test"}}
    with open(personal_info_file, "w") as f:
        yaml.dump(data, f)

    with pytest.raises(DataError, match="must contain 'personal_info' key"):
        load_personal_info(tmp_path)


def test_load_personal_info_validation_error(tmp_path: Path) -> None:
    """Test loading personal info with invalid data."""
    personal_info_file = tmp_path / "personal_info.yml"
    # Missing required 'name' field
    data = {"personal_info": {"email": "test@example.com"}}
    with open(personal_info_file, "w") as f:
        yaml.dump(data, f)

    with pytest.raises(DataError, match="Validation failed"):
        load_personal_info(tmp_path)


def test_load_shared_data_not_found() -> None:
    """Test loading from non-existent directory."""
    with pytest.raises(ConfigError):
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


def test_load_shared_data_invalid_data(tmp_path: Path) -> None:
    """Test loading shared data with invalid item data."""
    exp_file = tmp_path / "experiences.yml"
    # Missing required 'title' field
    exp_data = {
        "experiences": {
            "EXP1": {
                "company": "TechCo",
                "date": "2020",
            }
        }
    }
    with open(exp_file, "w") as f:
        yaml.dump(exp_data, f)

    with pytest.raises(DataError, match="Validation failed"):
        load_shared_data(tmp_path)


def test_load_shared_data_with_profiles(tmp_path: Path) -> None:
    """Test loading shared data including profiles."""
    profiles_file = tmp_path / "profiles.yml"
    profiles_data = {
        "profiles": {
            "TEST_PROFILE": {
                "title": "Test Title",
                "summary": "Test summary",
                "experiences": [],
                "projects": [],
            }
        }
    }
    with open(profiles_file, "w") as f:
        yaml.dump(profiles_data, f)

    shared = load_shared_data(tmp_path)
    assert "TEST_PROFILE" in shared.profiles
    assert shared.profiles["TEST_PROFILE"].title == "Test Title"


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

    with pytest.raises(DataError, match="Profile 'MISSING' not found"):
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

    with pytest.raises(DataError):
        build_resume_context(personal_info, "TEST", shared)
