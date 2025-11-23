"""Tests for resume generator."""

import pytest
from pathlib import Path

from resumodel.generator import ResumeGenerator
from resumodel.models import PersonalInfo


def test_generator_init_valid(tmp_path: Path) -> None:
    """Test initializing generator with valid template."""
    template_file = tmp_path / "template.tex.j2"
    template_file.write_text("Hello {{ name }}")

    generator = ResumeGenerator(template_file)
    assert generator.template_path == template_file


def test_generator_init_missing_template() -> None:
    """Test initializing with missing template."""
    with pytest.raises(FileNotFoundError):
        ResumeGenerator(Path("/nonexistent/template.tex"))


def test_generator_generate_simple(tmp_path: Path) -> None:
    """Test generating simple template."""
    from resumodel.models import TemplateContext, ResumeSections

    template_file = tmp_path / "template.tex.j2"
    template_file.write_text("Name: {{ personal_info.name }}\nTitle: {{ title }}")

    generator = ResumeGenerator(template_file)
    context = TemplateContext(
        personal_info=PersonalInfo(name="John Doe"),
        title="Engineer",
        summary="Test",
        sections=ResumeSections(),
    )
    result = generator.generate(context)

    assert "Name: John Doe" in result
    assert "Title: Engineer" in result


def test_generator_generate_with_loops(tmp_path: Path) -> None:
    """Test generating template with loops."""
    from resumodel.models import TemplateContext, ResumeSections, Experience

    template_file = tmp_path / "template.tex.j2"
    template_content = """
{% for exp in sections.experiences %}
- {{ exp.title }}
{% endfor %}
"""
    template_file.write_text(template_content)

    generator = ResumeGenerator(template_file)
    context = TemplateContext(
        personal_info=PersonalInfo(name="Test"),
        title="Test",
        summary="Test",
        sections=ResumeSections(
            experiences=[
                Experience(title="First", company="A", date="2020"),
                Experience(title="Second", company="B", date="2021"),
                Experience(title="Third", company="C", date="2022"),
            ]
        ),
    )
    result = generator.generate(context)

    assert "- First" in result
    assert "- Second" in result
    assert "- Third" in result


def test_generator_generate_to_file(tmp_path: Path) -> None:
    """Test generating resume to file."""
    from resumodel.models import TemplateContext, ResumeSections

    template_file = tmp_path / "template.tex.j2"
    template_file.write_text("Content: {{ summary }}")

    output_file = tmp_path / "output" / "resume.tex"

    generator = ResumeGenerator(template_file)
    context = TemplateContext(
        personal_info=PersonalInfo(name="Test"),
        title="Test",
        summary="Test content",
        sections=ResumeSections(),
    )
    generator.generate_to_file(context, output_file)

    assert output_file.exists()
    assert "Content: Test content" in output_file.read_text()


def test_latex_escape() -> None:
    """Test LaTeX character escaping."""
    from resumodel.generator import ResumeGenerator

    # Test special characters
    assert ResumeGenerator._latex_escape("&") == r"\&"
    assert ResumeGenerator._latex_escape("%") == r"\%"
    assert ResumeGenerator._latex_escape("$") == r"\$"
    assert ResumeGenerator._latex_escape("#") == r"\#"
    assert ResumeGenerator._latex_escape("_") == r"\_"
    assert ResumeGenerator._latex_escape("Test & Co.") == r"Test \& Co."


def test_generator_with_personal_info(tmp_path: Path) -> None:
    """Test generator with PersonalInfo model."""
    from resumodel.models import TemplateContext, ResumeSections

    template_file = tmp_path / "template.tex.j2"
    template_content = """
Name: {{ personal_info.name }}
Email: {{ personal_info.email }}
"""
    template_file.write_text(template_content)

    generator = ResumeGenerator(template_file)
    personal = PersonalInfo(
        name="Jane Doe",
        email="jane@example.com",
    )
    context = TemplateContext(
        personal_info=personal,
        title="Test Title",
        summary="Test Summary",
        sections=ResumeSections(),
    )
    result = generator.generate(context)

    assert "Name: Jane Doe" in result
    assert "Email: jane@example.com" in result
