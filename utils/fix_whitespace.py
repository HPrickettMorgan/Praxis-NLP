#!/usr/bin/env python3
"""A command line utility to fix whitespacing in scraped PDFs for Praxis-NLP."""
import argparse
from pathlib import Path
import re

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("file", help="file to clean", type=str)
    PARSER.add_argument("-o", "--output", help="output file", type=str)
    args = PARSER.parse_args()

    input_file = Path(args.file)
    output_file = Path(args.output) if args.output else None

    BLANK_LINE = re.compile(r"^\s*\n")
    EXTRA_WHITESPACE = re.compile(r"(?<!\.|:)\n| +[a-z]+$")

    with input_file.open("r") as f:
        s = "\n".join(line.strip() for line in f if line.strip())
        print(re.search(EXTRA_WHITESPACE, s))
        s, __ = re.subn(EXTRA_WHITESPACE, "", s)
        s = s.replace("\u2000", "")

    if not output_file:
        print(s)
    else:
        with output_file.open("w+") as f:
            f.write(s)

