"""YAML loading and data resolution."""

from pathlib import Path
from typing import Any, TypeVar
import yaml
from pydantic import BaseModel, ValidationError

from resumodel.models import (
    SharedData,
    Profile,
    Experience,
    Project,
    Education,
    Certification,
    ResearchPaper,
    ClubActivity,
    Hobby,
    PersonalInfo,
)
from resumodel.models import TemplateContext

T = TypeVar("T", bound=BaseModel)


def load_yaml(filepath: Path, model: type[T]) -> T:
    """Load and validate YAML file against a Pydantic model.

    Args:
        filepath: Path to YAML file
        model: Pydantic model class to validate against

    Returns:
        Validated model instance

    Raises:
        FileNotFoundError: If file doesn't exist
        ValidationError: If YAML doesn't match model schema
        yaml.YAMLError: If YAML is invalid
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Config file not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if data is None:
        raise ValueError(f"Empty YAML file: {filepath}")

    try:
        return model.model_validate(data)
    except ValidationError:
        raise


def load_personal_info(data_dir: Path) -> PersonalInfo:
    """Load personal info from personal_info.yml in the given directory.

    Args:
        data_dir: Directory containing personal_info.yml

    Returns:
        PersonalInfo instance

    Raises:
        FileNotFoundError: If personal_info.yml doesn't exist
        ValueError: If file is empty or missing personal_info key
    """
    filepath = data_dir / "personal_info.yml"
    if not filepath.exists():
        raise FileNotFoundError(f"Personal info file not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not data or "personal_info" not in data:
        raise ValueError("personal_info.yml must contain 'personal_info' key")

    return PersonalInfo.model_validate(data["personal_info"])


def load_shared_data(data_dir: Path) -> SharedData:
    """Load shared resume data from YAML files in the given directory.

    Args:
        data_dir: Directory containing YAML data files

    Returns:
        SharedData instance with loaded data

    Raises:
        FileNotFoundError: If directory doesn't exist
    """
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    shared = SharedData()

    # Load each data type if file exists with proper model validation
    data_files: dict[str, tuple[str, type[BaseModel]]] = {
        "experiences.yml": ("experiences", Experience),
        "projects.yml": ("projects", Project),
        "education.yml": ("education", Education),
        "certifications.yml": ("certifications", Certification),
        "research_papers.yml": ("research_papers", ResearchPaper),
        "clubs_and_associations.yml": ("clubs_and_associations", ClubActivity),
        "hobbies.yml": ("hobbies", Hobby),
        "profiles.yml": ("profiles", Profile),
    }

    for filename, (attr_name, model_class) in data_files.items():
        filepath = data_dir / filename
        if not filepath.exists():
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if not data:
                continue
            if not isinstance(data, dict):
                continue

        # Get the root key (e.g., "experiences", "projects")
        for key, value in data.items():
            if not value:
                continue
            if not isinstance(value, dict):
                continue

            # Validate each item in the dictionary
            validated_items = {
                item_id: model_class.model_validate(item_data)
                for item_id, item_data in value.items()
            }
            setattr(shared, key, validated_items)

    return shared


def build_resume_context(
    personal_info: "PersonalInfo", profile_name: str, shared: SharedData
) -> TemplateContext:
    """Build template context from personal info, profile name, and shared data.

    Args:
        personal_info: Personal contact information
        profile_name: Name of the profile to use
        shared: Shared data repository

    Returns:
        Dictionary ready for template rendering

    Raises:
        ValueError: If profile or referenced items not found
    """
    # Get the profile
    profile = shared.profiles.get(profile_name)
    if not profile:
        raise ValueError(f"Profile '{profile_name}' not found in shared data")

    # Build context
    context: dict[str, Any] = {
        "personal_info": personal_info,
        "title": profile.title,
        "summary": profile.summary,
        "sections": {},
    }

    # Add skills if present
    if profile.skills:
        context["sections"]["skills"] = profile.skills

    # Resolve references for each section
    context["sections"]["experiences"] = [
        shared.experiences[exp_id] for exp_id in profile.experiences
    ]
    context["sections"]["projects"] = [
        shared.projects[proj_id] for proj_id in profile.projects
    ]
    context["sections"]["education"] = [
        shared.education[edu_id] for edu_id in profile.education
    ]
    context["sections"]["certifications"] = [
        shared.certifications[cert_id] for cert_id in profile.certifications
    ]
    context["sections"]["research_papers"] = [
        shared.research_papers[res_id] for res_id in profile.research_papers
    ]
    context["sections"]["clubs_and_associations"] = [
        shared.clubs_and_associations[club_id]
        for club_id in profile.clubs_and_associations
    ]
    context["sections"]["hobbies"] = [
        shared.hobbies[hobby_id] for hobby_id in profile.hobbies
    ]

    context_parsed = TemplateContext.model_validate(context)

    return context_parsed
