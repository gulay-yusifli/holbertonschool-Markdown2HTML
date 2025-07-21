#!/usr/bin/python3
'''
This project converts markdown to HTML
'''
import sys

if len(sys.argv) == 1:
    print("Usage: ./markdown2html.py README.md README.html")
    sys.exit(1)
