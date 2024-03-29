#!/usr/bin/env python
"""__main__.py: extract comments from PDF
"""

__version__ = "0.1"

# Copyright 2018-2020, 2023 Michael M. Hoffman <michael.hoffman@utoronto.ca>

from argparse import Namespace
from collections import defaultdict
from os import extsep
from pathlib import Path
import re
import sys
from typing import DefaultDict, Iterator, List, Optional, TextIO

from PyPDF2 import PageObject, PdfReader

try:
    from os import EX_OK  # type: ignore[attr-defined]
except ImportError:
    EX_OK = 0  # XXX: no longer necessary in Python >=3.11

# key: int (number of stars)
# value: list of strs
SeverityDict = DefaultDict[int, List[str]]

ENCODING = "utf-8"

OUT_EXT = "txt"
STRICT = False

SEVERITY_NAMES = {0: "Minor comments",
                  1: "Major comments"}

re_stars = re.compile(
    r"""^
    (?P<stars>\**)
    \s*
    (?P<comment>.*)
    $""", re.DOTALL | re.VERBOSE)


def iter_annot_contents(page: PageObject) -> Iterator[str]:
    annot_indirects = page.annotations
    if annot_indirects is None:
        return

    for annot_indirect in annot_indirects:
        annot = annot_indirect.get_object()

        try:
            yield annot["/Contents"]
        except KeyError:
            continue


def load_comments(filename: str) -> SeverityDict:
    res: SeverityDict = defaultdict(list)

    reader = PdfReader(filename, STRICT)

    # In enumerate(reader.pages, 1), the 1 makes pages printed 1-based instead
    # of 0-based, as is used by all user-facing PDF software
    for page_num_1based, page in enumerate(reader.pages, 1):
        for contents in iter_annot_contents(page):
            m_stars = re_stars.match(contents)
            assert m_stars is not None  # should always match

            stars = m_stars["stars"]
            comment = m_stars["comment"]

            # number of stars
            severity = len(stars)

            res[severity].append(f"p{page_num_1based}: {comment}")

    return res


def get_severity_name(severity: int) -> str:
    return SEVERITY_NAMES.get(severity, f"Comments, severity {severity}")


def write_comments(severity: int, comments: List[str], file: TextIO) -> None:
    print(get_severity_name(severity), ":", sep="", file=file)

    print(file=file)
    print(*comments, sep="\n", file=file)
    print(file=file)


def save_comments(severities: SeverityDict, filename: str) -> None:
    with open(filename, "w") as file:
        for severity, comments in sorted(severities.items(), reverse=True):
            write_comments(severity, comments, file)


def pdfcomments(infilename: str, outfilename: Optional[str] = None) -> int:
    severities = load_comments(infilename)

    if outfilename is None:
        outfilename = extsep.join([Path(infilename).stem, OUT_EXT])

    save_comments(severities, outfilename)

    return EX_OK


def parse_args(args: List[str]) -> Namespace:
    from argparse import ArgumentParser

    description = __doc__.splitlines()[0].partition(": ")[2]
    parser = ArgumentParser(description=description)
    parser.add_argument("infile", help="input PDF file")
    parser.add_argument("outfile", nargs="?",
                        help="output text file"
                        " (default: infile with extension changed to 'txt')")

    version = f"%(prog)s {__version__}"
    parser.add_argument("--version", action="version", version=version)

    return parser.parse_args(args)


def main(argv: List[str] = sys.argv[1:]) -> int:
    args = parse_args(argv)

    return pdfcomments(args.infile, args.outfile)


if __name__ == "__main__":
    sys.exit(main())
