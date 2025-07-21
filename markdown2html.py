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
