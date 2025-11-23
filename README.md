# MTeck Resume Parser

[![CI](https://github.com/Hermann-web/mteck-resume-parser/actions/workflows/ci.yml/badge.svg)](https://github.com/Hermann-web/mteck-resume-parser/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A type-safe resume generator that creates LaTeX resumes from YAML data files using Jinja2 templates.

## Features

- **Type-Safe**: Full Pydantic validation for all resume data
- **Flexible**: Support for multiple profiles from the same personal data
- **Self-Contained**: Each resume example includes all its own data
- **Template-Based**: Use Jinja2 templates for complete layout control
- **CLI**: Simple command-line interface

## Installation

```bash
# Install with uv (recommended)
uv sync

# Or with pip
pip install -e .
```

## Quick Start

Generate a resume by specifying:
- `-d`: Data directory containing your YAML files
- `-p`: Profile name (from profiles.yml)
- `-t`: LaTeX template
- `-o`: Output file

```bash
# Generate Backend Developer resume  
resumodel -d examples/jane_doe \
  -p DEVBACKEND \
  -t templates/resume.tex.j2 \
  -o output/resume.tex
```

## Directory Structure

Each resume example is self-contained:

```
examples/jane_doe/
├── personal_info.yml          # Personal contact information
├── profiles.yml               # Profile definitions (DATASCIENTIST, etc.)
├── experiences.yml            # Work experiences
├── projects.yml               # Projects
├── education.yml              # Education history
├── certifications.yml         # Certifications
├── research_papers.yml        # Research papers
├── clubs_and_associations.yml # Clubs & associations
└── hobbies.yml                # Hobbies
```

## YAML File Formats

### personal_info.yml

```yaml
personal_info:
  name: "Your Name"
  phone: "+1 234 567 8900"
  email: "your.email@example.com"
  linkedin: "https://linkedin.com/in/yourprofile"
  github: "https://github.com/yourusername"
  location: "City, Country"
```

### profiles.yml

Define multiple resume profiles:

```yaml
profiles:
  DATASCIENTIST:
    title: "Data Scientist & ML Engineer"
    summary: "Experienced data scientist..."
    skills:
      - category: "Machine Learning"
        items: ["Python", "TensorFlow", "PyTorch"]
    experiences: ["EXP1", "EXP2"]  # Reference IDs
    projects: ["PROJ1", "PROJ2"]
    education: ["EDU1"]
    certifications: []
    research_papers: []
    clubs_and_associations: []
    hobbies: []
```

### experiences.yml

```yaml
experiences:
  EXP1:
    title: "Senior Data Scientist"
    company: "Tech Corp"
    date: "Jan 2020 - Present"
    location: "San Francisco, CA"
    bullet_points:
      - "Built ML models for recommendation system"
      - "Improved accuracy by 25%"
```

### projects.yml

```yaml
projects:
  PROJ1:
    name: "Awesome Project"
    link: "https://github.com/user/project"
    description: "Description of the project"
```

## Development

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run tests
uv run pytest tests/ -v

# Type checking
uv run mypy src/resumodel/

# Run formatter
uv run ruff format src/ tests/
```

## Project Structure

```
mteck-resume-parser/
├── src/resumodel/
│   ├── __init__.py
│   ├── cli.py          # Command-line interface
│   ├── models.py       # Pydantic models
│   ├── loader.py       # YAML loading & validation
│   └── generator.py    # Jinja2 template rendering
├── examples/
│   ├── hermann/        # Example 1 (self-contained)
│   └── jane_backend/   # Example 2 (self-contained)
├── templates/
│   └── resume.tex.j2   # LaTeX template
├── tests/
│   ├── test_models.py
│   ├── test_loader.py
│   └── test_generator.py
└── pyproject.toml
```

## Creating Your Own Resume

1. **Create a directory** for your resume (e.g., `examples/yourname/`)

2. **Add personal_info.yml**:
   ```yaml
   personal_info:
     name: "Your Name"
     email: "your@email.com"
     # ... other fields
   ```

3. **Create data files** (experiences.yml, projects.yml, etc.)

4. **Define profiles** in profiles.yml

5. **Generate**:
   ```bash
   resumodel -d examples/yourname -p YOURPROFILE \
     -t templates/resume.tex.j2 -o output/yourname.tex
   ```

## License

This project uses two licenses:
1. Code is released under the MIT License.
2. Resume templates and derived text are provided under CC BY 4.0 and require attribution.
