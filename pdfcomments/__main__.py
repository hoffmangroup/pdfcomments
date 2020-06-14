#!/usr/bin/env python
"""__main__.py: extract comments from PDF
"""

__version__ = "0.1"

# Copyright 2018-2020 Michael M. Hoffman <michael.hoffman@utoronto.ca>

from argparse import Namespace
from collections import defaultdict
from os import extsep, EX_OK
from pathlib import Path
import re
import sys
from typing import DefaultDict, Iterator, List, Optional, TextIO

from PyPDF2 import PdfFileReader
from PyPDF2.pdf import PageObject

# monkey-patching to fix
# https://github.com/mstamy2/PyPDF2/issues/151
from PyPDF2 import generic

PDF_DOC_ENCODING = list(generic._pdfDocEncoding)
PDF_DOC_ENCODING[9] = "\u0009"
PDF_DOC_ENCODING[10] = "\u000a"
PDF_DOC_ENCODING[13] = "\u000d"

generic._pdfDocEncoding = tuple(PDF_DOC_ENCODING)

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
    try:
        annot_indirects = page["/Annots"]
    except KeyError:
        return

    for annot_indirect in annot_indirects:
        annot = annot_indirect.getObject()

        try:
            yield annot["/Contents"]
        except KeyError:
            continue


def load_comments(filename: str) -> SeverityDict:
    res: SeverityDict = defaultdict(list)

    reader = PdfFileReader(filename, STRICT)
    for page_num, page in enumerate(reader.pages, 1):
        for contents in iter_annot_contents(page):
            m_stars = re_stars.match(contents)
            assert m_stars is not None  # should always match

            stars = m_stars["stars"]
            comment = m_stars["comment"]

            # number of stars
            severity = len(stars)

            res[severity].append(f"p{page_num}: {comment}")

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
