#!/usr/bin/python3
"""
markdown2html.py

Convert a markdown file to HTML format.

Usage:
  ./markdown2html.py input.md output.html
"""
import sysif len(sys.argv) < 3:
    print("Usage: ./markdown2html.py README.md README.html")
    exit(1)
