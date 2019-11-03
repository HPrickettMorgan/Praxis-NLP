#!/usr/bin/env python3
"""A command line utility to clean text files generated from PDFs for Praxis-NLP."""
import argparse
from pathlib import Path
import re

# match expressions in square or round brackets containing alphanumeric
# characters or spaces
BRACKET_REGEX = re.compile(r'\s?\[(\w|\s|,)*\]|\s?\((\w|\s|,)*\)')
BIB_REGEX = re.compile(
    r'(Bibliography)|(Works Cited)|(Source Extracts)|(Appendix(:|\n))', re.IGNORECASE
)
EXTRA_WHITESPACE = re.compile(r" [a-z\)\],;]+\n")


def remove_non_ascii(s):
    """Re-encodes s as ASCII"""
    s.encode('ascii', 'ignore')
    return s


def remove_citations(s, verbose=False):
    """Removes anything between brackets, or after a bibliograhpy heading"""
    lines = []
    characters_written = 0
    characters_read = 0

    for line_number, line in enumerate(s.split('\n')):

        if re.search(BIB_REGEX, line):
            if verbose:
                print(f'Truncated at line {line_number}: {line}')
            break
        (new_line, __) = re.subn(BRACKET_REGEX, '', line)
        lines.append(new_line)
        characters_read += len(line)
        characters_written += len(new_line)

    return ('\n'.join(lines), (characters_read - characters_written) / characters_read)


def fix_whitespace(s):
    """Removes superfluous lines and newlines"""
    s = '\n'.join(
        line.strip(' -\t\n') for line in s.split('\n') if line.strip(' -\t\n123456789.')
    )
    s, __ = re.subn(EXTRA_WHITESPACE, ' ', s)

    # remove weird characters
    s = s.replace(u'\u200b', '')

    # merge lines with line breaks in the middle and a lower case letter at the beggining
    # of the next line, indicating that there has been a line break mid-sentence
    s_list = s.split('\n')
    lines = []

    j = 0
    for i, line in enumerate(s_list):

        is_continuation_line = False
        split_line = line.split()
        is_continuation_line = \
            i > 0 \
            and len(split_line) > 3 \
            and split_line[0].islower()

        if not is_continuation_line:
            lines.append(line + '\n')
        else:
            j += 1
            lines[i-j] = lines[i-j].strip('\n') + ' ' + line + '\n'
    s = "".join(lines)

    return s


def clean_file(file, verbose=False):

    input_file = Path(file)
    with input_file.open(mode='r') as f:
        file_text = f.read()

    file_text = remove_non_ascii(file_text)
    file_text, percent_deleted = remove_citations(file_text, verbose)
    warn_deletion_threshold = 0.5
    if percent_deleted > warn_deletion_threshold:
        print(f'Warning: proportion of {file} deleted is {percent_deleted}')
    file_text = fix_whitespace(file_text)
    return file_text


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('file', help='file to clean', type=str)
    PARSER.add_argument('-o', '--output', help='output file', type=str)
    PARSER.add_argument(
        '-v', '--verbose', action='store_true', help='set verbosity of cleaning'
    )
    args = PARSER.parse_args()

    output_file = Path(args.output) if args.output else None

    out_text = clean_file(args.file, args.verbose)

    if output_file:
        with output_file.open(mode='w+') as f:
            f.write(out_text)
    else:
        print(out_text)
