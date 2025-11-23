"""Tests for CLI module."""

import pytest
from pathlib import Path
from unittest.mock import patch
import sys

from resumodel.cli import main


def test_cli_success(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Test successful resume generation via CLI."""
    # Create test data directory
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    # Create personal_info.yml
    personal_info = data_dir / "personal_info.yml"
    personal_info.write_text("""
personal_info:
  name: "Test User"
  email: "test@example.com"
  location: "Test City"
""")

    # Create experiences.yml
    experiences = data_dir / "experiences.yml"
    experiences.write_text("""
experiences:
  EXP1:
    title: "Engineer"
    company: "TestCo"
    date: "2020"
    location: "NYC"
""")

    # Create profiles.yml
    profiles = data_dir / "profiles.yml"
    profiles.write_text("""
profiles:
  TEST_PROFILE:
    title: "Test Title"
    summary: "Test summary"
    experiences:
      - "EXP1"
""")

    # Create template
    template_file = tmp_path / "template.tex.j2"
    template_file.write_text("{{ personal_info.name }}")

    # Create output file path
    output_file = tmp_path / "output.tex"

    # Mock sys.argv
    test_args = [
        "resumodel",
        "-d",
        str(data_dir),
        "-p",
        "TEST_PROFILE",
        "-t",
        str(template_file),
        "-o",
        str(output_file),
    ]

    with patch.object(sys, "argv", test_args):
        main()

    # Verify output file was created
    assert output_file.exists()
    assert "Test User" in output_file.read_text()


def test_cli_verbose_flag(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Test CLI with verbose flag enables debug logging."""
    # Create minimal test setup
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    personal_info = data_dir / "personal_info.yml"
    personal_info.write_text("""
personal_info:
  name: "Test User"
""")

    profiles = data_dir / "profiles.yml"
    profiles.write_text("""
profiles:
  TEST:
    title: "Title"
    summary: "Summary"
""")

    template_file = tmp_path / "template.tex.j2"
    template_file.write_text("{{ personal_info.name }}")

    output_file = tmp_path / "output.tex"

    test_args = [
        "resumodel",
        "-d",
        str(data_dir),
        "-p",
        "TEST",
        "-t",
        str(template_file),
        "-o",
        str(output_file),
        "-v",  # verbose flag
    ]

    with patch.object(sys, "argv", test_args):
        main()

    # Verify it ran successfully
    assert output_file.exists()


def test_cli_missing_data_dir() -> None:
    """Test CLI with non-existent data directory."""
    test_args = [
        "resumodel",
        "-d",
        "/nonexistent/path",
        "-p",
        "PROFILE",
        "-t",
        "template.tex.j2",
        "-o",
        "output.tex",
    ]

    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1


def test_cli_invalid_profile(tmp_path: Path) -> None:
    """Test CLI with invalid profile name."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    personal_info = data_dir / "personal_info.yml"
    personal_info.write_text("""
personal_info:
  name: "Test User"
""")

    profiles = data_dir / "profiles.yml"
    profiles.write_text("""
profiles:
  VALID_PROFILE:
    title: "Title"
    summary: "Summary"
""")

    template_file = tmp_path / "template.tex.j2"
    template_file.write_text("{{ personal_info.name }}")

    output_file = tmp_path / "output.tex"

    test_args = [
        "resumodel",
        "-d",
        str(data_dir),
        "-p",
        "INVALID_PROFILE",  # This profile doesn't exist
        "-t",
        str(template_file),
        "-o",
        str(output_file),
    ]

    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1


def test_cli_missing_template() -> None:
    """Test CLI with non-existent template file."""
    test_args = [
        "resumodel",
        "-d",
        ".",
        "-p",
        "PROFILE",
        "-t",
        "/nonexistent/template.tex.j2",
        "-o",
        "output.tex",
    ]

    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1


def test_cli_unexpected_error(tmp_path: Path) -> None:
    """Test CLI handles unexpected errors gracefully."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    personal_info = data_dir / "personal_info.yml"
    personal_info.write_text("""
personal_info:
  name: "Test User"
""")

    test_args = [
        "resumodel",
        "-d",
        str(data_dir),
        "-p",
        "PROFILE",
        "-t",
        "template.tex.j2",
        "-o",
        "output.tex",
    ]

    # This will cause an unexpected error (profiles.yml doesn't exist)
    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
