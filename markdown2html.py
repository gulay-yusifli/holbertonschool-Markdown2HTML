#!/usr/bin/python3
"""
markdown2html.py

Converts Markdown to HTML:
- Headings (#)
- Unordered lists (-)
- Ordered lists (*)
- Paragraphs
- Bold (**...**) → <b>
- Emphasis (__...__) → <em>
- [[text]] → md5(text)
- ((text)) → remove 'c' or 'C' from text

Usage:
    ./markdown2html.py README.md README.html
"""

import sys
import os
import re
import hashlib


def print_usage_and_exit():
    """Print usage message and exit with code 1."""
    print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
    sys.exit(1)


def apply_inline_formatting(line):
    """
    Apply inline formatting:
    - bold (**text**) → <b>
    - emphasis (__text__) → <em>
    - [[text]] → md5 hash of text
    - ((text)) → remove all 'c' or 'C' from text
    """

    line = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
    line = re.sub(r'__(.+?)__', r'<em>\1</em>', line)

    def remove_c(match):
        content = match.group(1)
        return re.sub(r'[cC]', '', content)

    line = re.sub(r'\(\((.+?)\)\)', remove_c, line)

    def md5_hash(match):
        content = match.group(1)
        h = hashlib.md5(content.encode('utf-8')).hexdigest()
        return h

    line = re.sub(r'\[\[(.+?)\]\]', md5_hash, line)

    return line


def convert_markdown_to_html(input_file, output_file):
    """Convert markdown file content to HTML format."""

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

        if (stripped.startswith('#') or stripped.startswith('- ') or
                stripped.startswith('* ') or stripped == ''):
            if in_paragraph:
                output_lines.append('<p>')
                for i, pline in enumerate(paragraph_lines):
                    if i > 0:
                        output_lines.append('<br/>')
                    output_lines.append(apply_inline_formatting(pline))
                output_lines.append('</p>')
                paragraph_lines = []
                in_paragraph = False

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
                output_lines.append(
                    f"<h{level}>{apply_inline_formatting(content)}</h{level}>"
                )
                continue

        if stripped.startswith('- '):
            if in_ol:
                output_lines.append('</ol>')
                in_ol = False
            if not in_ul:
                output_lines.append('<ul>')
                in_ul = True
            content = stripped[2:].strip()
            output_lines.append(f"<li>{apply_inline_formatting(content)}</li>")
            continue

        if stripped.startswith('* '):
            if in_ul:
                output_lines.append('</ul>')
                in_ul = False
            if not in_ol:
                output_lines.append('<ol>')
                in_ol = True
            content = stripped[2:].strip()
            output_lines.append(f"<li>{apply_inline_formatting(content)}</li>")
            continue

        if stripped == '':
            if in_ul:
                output_lines.append('</ul>')
                in_ul = False
            if in_ol:
                output_lines.append('</ol>')
                in_ol = False
            continue

        paragraph_lines.append(stripped)
        in_paragraph = True

    if in_ul:
        output_lines.append('</ul>')
    if in_ol:
        output_lines.append('</ol>')
    if in_paragraph:
        output_lines.append('<p>')
        for i, pline in enumerate(paragraph_lines):
            if i > 0:
                output_lines.append('<br/>')
            output_lines.append(apply_inline_formatting(pline))
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
