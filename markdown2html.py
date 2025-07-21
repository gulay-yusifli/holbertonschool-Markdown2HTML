#!/usr/bin/python3
"""
markdown2html.py

A script that converts Markdown headings (# to ######) into HTML tags.

Usage:
    ./markdown2html.py README.md README.html
"""

import sys
import os


def print_usage_and_exit():
    """Print usage message and exit with code 1."""
    print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
    sys.exit(1)


def convert_markdown_to_html(input_file, output_file):
    """Read the input file, convert Markdown headings to HTML, and write output."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {input_file}: {e}", file=sys.stderr)
        sys.exit(1)

    output_lines = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip('#'))
            if 1 <= level <= 6 and stripped[level:level+1] == ' ':
                content = stripped[level:].strip()
                html_line = f"<h{level}>{content}</h{level}>"
                output_lines.append(html_line)
            else:
                output_lines.append(line.rstrip())
        else:
            output_lines.append(line.rstrip())

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_lines))
    except Exception as e:
        print(f"Error writing to {output_file}: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main execution logic."""
    if len(sys.argv) < 3:
        print_usage_and_exit()

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    convert_markdown_to_html(input_file, output_file)
    sys.exit(0)


if __name__ == "__main__":
    main()
