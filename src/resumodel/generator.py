# Copyright (c) 2025 Hermann Agossou
# Licensed under the MIT License. See the LICENSE file for details.

"""Resume generation with Jinja2 templates."""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from resumodel.models import TemplateContext
from resumodel.exceptions import TemplateError
from resumodel.logging import logger


class ResumeGenerator:
    """Generate resumes from templates and context data."""

    def __init__(self, template_path: Path) -> None:
        """Initialize generator with template.

        Args:
            template_path: Path to Jinja2 template file

        Raises:
            TemplateError: If template file not found
        """
        self.template_path = template_path
        if not template_path.exists():
            raise TemplateError(f"Template not found: {template_path}")

        # Set up Jinja2 environment
        template_dir = template_path.parent
        logger.debug(f"Initializing Jinja2 environment in {template_dir}")

        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Add custom filters for LaTeX escaping
        self.env.filters["latex_escape"] = self._latex_escape

        try:
            self.template = self.env.get_template(template_path.name)
        except TemplateNotFound as e:
            raise TemplateError(
                f"Failed to load template {template_path.name}: {e}"
            ) from e

    @staticmethod
    def _latex_escape(text: str) -> str:
        """Escape special LaTeX characters.

        Args:
            text: Text to escape

        Returns:
            Escaped text safe for LaTeX
        """
        # Handle backslash first to avoid double-escaping
        replacements = [
            ("\\", r"\textbackslash{}"),
            ("&", r"\&"),
            ("%", r"\%"),
            ("$", r"\$"),
            ("#", r"\#"),
            ("_", r"\_"),
            ("{", r"\{"),
            ("}", r"\}"),
            ("~", r"\textasciitilde{}"),
            ("^", r"\^{}"),
        ]
        for old, new in replacements:
            text = text.replace(old, new)
        return text

    def generate(self, context: TemplateContext) -> str:
        """Generate resume content from context.

        Args:
            context: Template context data

        Returns:
            Rendered template content

        Raises:
            TemplateError: If rendering fails
        """
        logger.debug("Rendering template...")
        try:
            return self.template.render(context)
        except Exception as e:
            raise TemplateError(f"Failed to render template: {e}") from e

    def generate_to_file(self, context: TemplateContext, output_path: Path) -> None:
        """Generate resume and write to file.

        Args:
            context: Template context data
            output_path: Output file path
        """
        content = self.generate(context)

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(f"Generated resume: {output_path}")
