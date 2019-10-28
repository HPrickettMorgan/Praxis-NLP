#!/usr/bin/env python3
"""A command line utility to text files generated from PDFs for Praxis-NLP."""
import argparse
from pathlib import Path
import sys
import re

bracket_regex = re.compile(r"\s?\[\d*\]\s?")
bib_regex = r""

parser = argparse.ArgumentParser()
parser.add_argument("file", help="file to clean", type=str)
parser.add_argument("-o", "--output", help="output file", type=str)
parser.add_argument("-v", "--verbosity", help="0: silent, 1: percent removed, 2: print each deletion", type=int)
args = parser.parse_args()

if not args.verbosity:
    args.verbosity = 0
elif args.verbosity < 0 or args.verbosity > 2:
    args.verbosity = 0
    print("Invalid verbosity was given, defaulting to 0")

input_file = Path(args.file)
if args.output:
    output_file = Path(args.output)
else:
    output_file = input_file.parent / (input_file.stem +  "_clean" + input_file.suffix)
    
if args.verbosity > 0:
    characters_written = 0
    characters_read = 0

with input_file.open(mode="r") as in_file, output_file.open(mode="w") as out_file:

    for line_number, line in enumerate(in_file):
        if args.verbosity == 2:
            deleted = re.findall(bracket_regex, line)
            if deleted:
                print(f"Line {line_number}: {', '.join(deleted)}")
        (new_line, __) = re.subn(bracket_regex, "", line)
        
        if args.verbosity > 0:
            characters_read += len(line)
            characters_written += len(new_line)
        
        out_file.write(new_line)

if(args.verbosity > 0):
    print(f"Deleted {(characters_read - characters_written)/ characters_read}% of the file")    