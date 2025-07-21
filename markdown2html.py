#!/usr/bin/python3
"""
markdown2html.py

A script that converts Markdown to HTML:
- Headings (#, ##, ..., ######)
- Unordered lists (-)
- Ordered lists (*)
- Paragraphs (single or multiline)

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
    Convert markdown to HTML: headings, unordered/ordered lists, paragraphs.
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
    in_paragraph = False
    paragraph_lines = []

    for line in lines:
        stripped = line.strip()

        # Close paragraph before handling other block types
        if stripped.startswith('#') or stripped.startswith('- ') or \
           stripped.startswith('* ') or stripped == '':
            if in_paragraph:
                output_lines.append('<p>')
                for i, pline in enumerate(paragraph_lines):
                    if i > 0:
                        output_lines.append('<br/>')
                    output_lines.append(pline)
                output_lines.append('</p>')
                paragraph_lines = []
                in_paragraph = False

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

        # Unordered list
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

        # Ordered list
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

        # Blank line — close any open lists
        if stripped == '':
            if in_ul:
                output_lines.append('</ul>')
                in_ul = False
            if in_ol:
                output_lines.append('</ol>')
                in_ol = False
            continue

        # Paragraph content
        paragraph_lines.append(stripped)
        in_paragraph = True

    # Final cleanup: close any still-open tags
    if in_ul:
        output_lines.append('</ul>')
    if in_ol:
        output_lines.append('</ol>')
    if in_paragraph:
        output_lines.append('<p>')
        for i, pline in enumerate(paragraph_lines):
            if i > 0:
                output_lines.append('<br/>')
            output_lines.append(pline)
        output_lines.append('</p>')

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
