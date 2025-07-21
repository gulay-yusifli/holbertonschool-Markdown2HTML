#!/usr/bin/python3
"""
markdown2html.py

A script that converts Markdown headings, unordered (-),
and ordered (*) lists into corresponding HTML.

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
    """
    Convert markdown to HTML: headings, unordered (-) and ordered (*) lists.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {input_file}: {e}", file=sys.stderr)
        sys.exit(1)

    output_lines = []
    in_ul = False
    in_ol = False

    for line in lines:
        stripped = line.strip()

        # Headings
        if stripped.startswith('#'):
            level = len(stripped) - len(stripped.lstrip('#'))
            if 1 <= level <= 6 and stripped[level:level + 1] == ' ':
                if in_ul:
                    output_lines.append('</ul>')
                    in_ul = False
                if in_ol:
                    output_lines.append('</ol>')
                    in_ol = False
                content = stripped[level:].strip()
                output_lines.append(f"<h{level}>{content}</h{level}>")
                continue

        # Unordered list item (-)
        if stripped.startswith('- '):
            if in_ol:
                output_lines.append('</ol>')
                in_ol = False
            if not in_ul:
                output_lines.append('<ul>')
                in_ul = True
            content = stripped[2:].strip()
            output_lines.append(f"<li>{content}</li>")
            continue

        # Ordered list item (*)
        if stripped.startswith('* '):
            if in_ul:
                output_lines.append('</ul>')
                in_ul = False
            if not in_ol:
                output_lines.append('<ol>')
                in_ol = True
            content = stripped[2:].strip()
            output_lines.append(f"<li>{content}</li>")
            continue

        # Blank line closes lists
        if stripped == '':
            if in_ul:
                output_lines.append('</ul>')
                in_ul = False
            if in_ol:
                output_lines.append('</ol>')
                in_ol = False

    # Close any open list at end of file
    if in_ul:
        output_lines.append('</ul>')
    if in_ol:
        output_lines.append('</ol>')

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
