#!/usr/bin/python3

import sys
import os

def main():
    with open("README.html", "w") as output:
        with open(sys.argv[1], 'r') as file:
            for l in file.readlines():
                num = l.count('#')
                text = l.replace("#", "")[1:-1]
                new_line = f"<h{num}>{text}</h{num}>"
                output.write(new_line + "\n")


if __name__ == "__main__":
    main()
