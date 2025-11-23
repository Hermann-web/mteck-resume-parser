# Integration Notes

## Project Overview

MTeck Resume Parser is a resume generator that creates LaTeX resumes from YAML data files using Jinja2 templates.

## Usage

### Generating New Resume Data

1. Create a new directory under `examples/` for each person
2. Use the YAML structure defined in the README
3. Ensure all referenced IDs in `profiles.yml` match entries in other YAML files

### Data Validation

The project uses Pydantic models for type-safe validation. All YAML data is validated against these models during loading.

### Example Commands

Read the [README](README.md) for example commands.

## CI/CD Requirements

The project uses GitHub Actions for continuous integration. All PRs and commits to `main` must pass the following checks:

### Test Matrix

- **Python Versions**: 3.10, 3.11, 3.12, 3.13
- **Platform**: Ubuntu Latest

### Quality Checks (All Must Pass)

1. **Tests with Coverage**
   ```bash
   uv run pytest tests/ -v --cov=src/resumodel --cov-report=xml --cov-report=term
   ```
   - All tests must pass
   - Coverage report uploaded to Codecov (Python 3.11 only)

2. **Type Checking with mypy** ✓ **REQUIRED**
   ```bash
   uv run mypy src/resumodel/
   ```
   - Strict mode enabled
   - All type errors must be resolved
   - Configuration in `[tool.mypy]` section of `pyproject.toml`

3. **Code Formatting with ruff** ✓ **REQUIRED**
   ```bash
   # Check formatting (CI)
   uv run ruff format --check .
   
   # Auto-format (local development)
   uv run ruff format .
   ```
   - Code must be formatted according to ruff standards
   - Run formatter before committing

4. **Linting with ruff** ✓ **REQUIRED**
   ```bash
   uv run ruff check .
   ```
   - All linting errors must be fixed
   - ruff handles both formatting and linting

### Local Development Workflow

Before pushing code, ensure all checks pass:

```bash
# Run all checks
uv run pytest tests/ -v
uv run pytest --cov=src/resumodel --cov-report=term-missing tests/
uv run mypy src/resumodel/
uv run ruff format .
uv run ruff check .
```

Or use a pre-commit hook to automate these checks.

## Tips for Development

1. **Maintain Type Safety**: Always update Pydantic models when adding new fields
2. **Self-Contained Examples**: Each example directory should be completely independent
3. **Consistent Naming**: Use uppercase IDs with underscores (e.g., `TECH_GIANT_SENIOR`)
4. **Reference Integrity**: Ensure profile references point to existing entries
5. **Run Quality Checks**: Always run mypy and ruff before committing
6. **Type Annotations**: All functions must have complete type annotations (mypy strict mode)

## Future Enhancements

- [ ] Add more template options
- [ ] Support for PDF generation directly
- [ ] Web interface for YAML editing
- [ ] Automated validation scripts
- [ ] Example data for more diverse career paths
