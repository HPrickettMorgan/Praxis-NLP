#!/usr/bin/env python3
"""A command line utility to clean text files generated from PDFs for Praxis-NLP."""
import argparse
from pathlib import Path
from sys import stderr
import re

BRACKET_REGEX = re.compile(r"\s?\[\w*\]\s?|\s?\(\w*\)\s?")
BIB_REGEX = re.compile(r"(Bibliography)|(Works Cited)|(Source Extracts)", re.IGNORECASE)
EXTRA_WHITESPACE = re.compile(r" [a-z\)\],;]+\n")


def remove_citations(s, verbose=False):
    """Removes anything between brackets, parentheses, or after a works cited heading"""
    lines=[]
    characters_written = 0
    characters_read = 0

    for line_number, line in enumerate(s.split('\n')):

        if re.search(BIB_REGEX, line):
            if verbose:
                print(f"Truncated at line {line_number}: {line}", file=stderr)
            break
        (new_line, __) = re.subn(BRACKET_REGEX, "", line)
        lines.append(new_line)
        characters_read += len(line)
        characters_written += len(new_line)

    characters_read += sum(len(line) for line in s)
    return ("\n".join(lines), (characters_read-characters_written)/characters_read)

def fix_whitespace(s):
    """Removes superfluous lines and newlines"""
    s = "\n".join(line.strip(" -\t\n") for line in s.split("\n") if line.strip(" -\t\n123456789."))
    s, __ = re.subn(EXTRA_WHITESPACE, " ", s)
    return s.replace("\u2000", "")

if __name__ ==  "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("file", help="file to clean", type=str)
    PARSER.add_argument("-o", "--output", help="output file", type=str)
    PARSER.add_argument("-v", "--verbose", action="store_true", help="set verbosity of cleaning")
    args = PARSER.parse_args()

    input_file = Path(args.file)
    output_file = Path(args.output) if args.output else None

    with input_file.open(mode="r") as f:
        out_text, percent_deleted = remove_citations(f.read(), args.verbose)
        out_text = fix_whitespace(out_text)
    
    if output_file:
        with output_file.open(mode="w+") as f:
            f.write(out_text)
    else:
        print(out_text)

    if args.verbose:
        print(f"Deleted {percent_deleted}% of the file", file=stderr)
