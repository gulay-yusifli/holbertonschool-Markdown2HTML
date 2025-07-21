#!/usr/bin/python3
"""
markdown2html.py

A script to validate and prepare conversion from Markdown to HTML.

Usage:
    ./markdown2html.py README.md README.html
"""

import sys
import os


def print_usage_and_exit():
    """Print usage message and exit with code 1."""
    print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
    sys.exit(1)


def main():
    """Main execution logic."""
    if len(sys.argv) < 3:
        print_usage_and_exit()

    input_file = sys.argv[1]

    if not os.path.isfile(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    # No output required on success
    sys.exit(0)


if __name__ == "__main__":
    main()
