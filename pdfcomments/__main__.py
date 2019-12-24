#!/usr/bin/env python
"""__init__.py: extract comments from PDF
"""

__version__ = "0.1"

# Copyright 2018, 2019 Michael M. Hoffman <michael.hoffman@utoronto.ca>

from argparse import Namespace
from collections import defaultdict
from os import extsep
from pathlib import Path
import re
import sys
from typing import DefaultDict, Iterator, List, Optional

from PyPDF2 import PageObject, PdfFileReader

# key: int (number of stars)
# value: list of strs
LevelsDict = DefaultDict[int, List[str]]

OUT_EXT = "txt"
STRICT = False

LEVEL_NAMES = {0: "Minor comments",
               1: "Major comments"}

re_stars = re.compile(
    r"""^
    (?P<stars>\**)
    \s*
    (?P<comment>.*)
    $""", re.VERBOSE)


def iter_annot_contents(page: PageObject) -> Iterator[str]:
    try:
        annot_indirects = page.annots["/Annots"]
    except KeyError:
        return

    for annot_indirect in annot_indirects:
        annot = annot_indirect.getObject()

        try:
            yield annot["/Contents"]
        except KeyError:
            continue

def load_comments(filename: str) -> LevelsDict:
    res = defaultdict(list)

    reader = PdfFileReader(filename, STRICT)
    for page_num, page in enumerate(reader.pages, 1):
        for contents in iter_annot_contents(page):
            m_stars = re_stars.match(contents)
            stars = m_stars["stars"]
            comment = m_stars["comment"]

            # number of stars
            level = len(stars)

            res[level].append(f"p{page_num}: {comment}")

    return res


def get_level_name(level: int) -> str:
    return LEVEL_NAMES.get(level, f"Comments, level {level}")


def save_comments(levels: LevelsDict, filename: str) -> None:
    with open(filename, "w") as outfile:
        for level in sorted(levels, reverse=True):
            print(get_level_name(level), ":", sep="", file=outfile)

            print(file=outfile)
            print(*levels[level], sep="\n", file=outfile)
            print(file=outfile)


def pdfcomments(infilename: str, outfilename: str = None) -> None:
    levels = load_comments(infilename)

    if outfilename is None:
        outfilename = extsep.join([Path(infilename).stem, OUT_EXT])

    return save_comments(levels, outfilename)


def parse_args(args: List[str]) -> Namespace:
    from argparse import ArgumentParser

    description = __doc__.splitlines()[0].partition(": ")[2]
    parser = ArgumentParser(description=description)
    parser.add_argument("infile", help="input file in PDF format")
    parser.add_argument("outfile", nargs="?",
                        help="output file"
                        " (default: infile with extension changed to 'txt')")

    version = f"%(prog)s {__version__}"
    parser.add_argument("--version", action="version", version=version)

    return parser.parse_args(args)


def main(argv: List[str] = sys.argv[1:]) -> Optional[int]:
    args = parse_args(argv)

    return pdfcomments(args.infile, args.outfile)


if __name__ == "__main__":
    sys.exit(main())
