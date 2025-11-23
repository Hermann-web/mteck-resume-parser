# Copyright (c) 2025 Hermann Agossou
# Licensed under the MIT License. See the LICENSE file for details.

"""Command-line interface for resume generation."""

import argparse
import sys
from pathlib import Path
from pydantic import ValidationError

from resumodel.loader import load_personal_info, load_shared_data, build_resume_context
from resumodel.generator import ResumeGenerator


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
  resumodel -d examples/jane_backend -p DEVBACKEND -t templates/resume.tex.j2 -o output/jane.tex
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

    args = parser.parse_args()

    try:
        # Load personal info
        print(f"Loading personal info from {args.data_dir}...")
        personal_info = load_personal_info(args.data_dir)

        # Load data from directory
        print(f"Loading data from {args.data_dir}...")
        shared = load_shared_data(args.data_dir)

        # Build context
        print(f"Building context for profile '{args.profile}'...")
        context = build_resume_context(personal_info, args.profile, shared)

        # Generate resume
        print(f"Rendering template {args.template}...")
        generator = ResumeGenerator(args.template)
        generator.generate_to_file(context, args.output)

        print(f"\n✓ Success! Resume generated at: {args.output}")

    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except ValidationError as e:
        print("ERROR: Configuration validation failed:", file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)
    except KeyError as e:
        print(f"ERROR: Missing reference: {e}", file=sys.stderr)
        print(
            "Check that all referenced IDs exist in shared data files.", file=sys.stderr
        )
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
