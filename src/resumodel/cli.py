# Copyright (c) 2025 Hermann Agossou
# Licensed under the MIT License. See the LICENSE file for details.

"""Command-line interface for resume generation."""

import argparse
import sys
import logging
from pathlib import Path

from resumodel.loader import load_personal_info, load_shared_data, build_resume_context
from resumodel.generator import ResumeGenerator
from resumodel.exceptions import ResuModelError
from resumodel.logging import setup_logging, logger


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate resumes from YAML data and Jinja2 templates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate Hermann's Data Scientist resume
  resumodel -d examples/hermann -p DATASCIENTIST -t templates/resume.tex.j2 -o output/hermann.tex

  # Generate Jane's Backend Developer resume
  resumodel -d examples/jane_doe -p SOFTWARE_ENGINEER -t templates/resume.tex.j2 -o output/jane.tex
        """,
    )

    parser.add_argument(
        "-d",
        "--data-dir",
        type=Path,
        required=True,
        help="Data directory containing personal_info.yml and other YAML files",
    )
    parser.add_argument(
        "-p",
        "--profile",
        type=str,
        required=True,
        help="Profile name to use (e.g., DATASCIENTIST, DEVBACKEND)",
    )
    parser.add_argument(
        "-t",
        "--template",
        type=Path,
        required=True,
        help="Path to Jinja2 template file",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        required=True,
        help="Output file path",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(level=log_level)

    try:
        # Load personal info
        logger.info(f"Loading personal info from {args.data_dir}...")
        personal_info = load_personal_info(args.data_dir)

        # Load data from directory
        logger.info(f"Loading data from {args.data_dir}...")
        shared = load_shared_data(args.data_dir)

        # Build context
        logger.info(f"Building context for profile '{args.profile}'...")
        context = build_resume_context(personal_info, args.profile, shared)

        # Generate resume
        logger.info(f"Rendering template {args.template}...")
        generator = ResumeGenerator(args.template)
        generator.generate_to_file(context, args.output)

        logger.info("Success!")

    except ResuModelError as e:
        logger.error(str(e))
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
