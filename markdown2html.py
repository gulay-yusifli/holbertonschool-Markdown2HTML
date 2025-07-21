#!/usr/bin/python3
"""
markdown2html.py

Convert a markdown file to HTML format.

Usage:
  ./markdown2html.py input.md output.html
"""
import sys
import os

def print_usage_and_exit():
    print("Usage: ./markdown2html.py README.md README.html")
    sys.exit(1)

def markdown_to_html(md_text):
    # Simple dummy converter: wrap lines in <p> tags
    # Replace this with a proper markdown parser if desired.
    lines = md_text.strip().splitlines()
    html_lines = [f"<p>{line}</p>" for line in lines if line.strip()]
    return "\n".join(html_lines)
