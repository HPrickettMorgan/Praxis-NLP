"""A command line utility to fix whitespacing in scraped PDFs for Praxis-NLP."""
import argparse
from pathlib import Path
import re
from sys import stdout

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("file", help="file to clean", type=str)
    PARSER.add_argument("-o", "--output", help="output file", type=str)
    args = PARSER.parse_args()

    input_file = Path(args.file)
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = stdout

    BLANK_LINE = re.compile(r"^\s*$")
    EXTRA_WHITESPACE = re.compile(r"(?<!\.|:|[A-Z]\w*)\n")

    with input_file.open("r") as f:
        s = f.read()
        s = re.subn(BLANK_LINE, "", s)
        s = re.subn(EXTRA_WHITESPACE, " ", s)
        s = "\n".join(line.strip().replace("\u2000", "") for line in s)

    with output_file.open("w+") as f:
        f.write(s)

