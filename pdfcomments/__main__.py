#!/usr/bin/env python
"""__init__.py: extract comments from PDF
"""

__version__ = "0.1"

# Copyright 2018, 2019 Michael M. Hoffman <michael.hoffman@utoronto.ca>

from argparse import Namespace
from collections import defaultdict
from os import extsep
import re
import sys
from typing import DefaultDict, List, Optional

from path import Path

from PyPDF2 import PdfFileReader

# key: int (number of stars)
# value: list of strs
LevelsDict = DefaultDict[int, List[str]]

OUT_EXT = "txt"
STRICT = False

re_stars = re.compile(r"^(?P<stars>\**) *(?P<comment>.*)$")


def load_comments(infilename: str) -> LevelsDict:
    res = defaultdict(list)

    reader = PdfFileReader(infilename, STRICT)
    for page_num, page in enumerate(reader.pages):
        try:
            annot_indirects = page["/Annots"]
        except KeyError:
            continue

        for annot_indirect in annot_indirects:
            annot = annot_indirect.getObject()

            try:
                contents = annot["/Contents"]
            except KeyError:
                continue

            m_stars = re_stars.match(contents)
            stars = m_stars["stars"]
            comment = m_stars["comment"]

            level = len(stars)

            res[level].append(f"p{page_num+1}: {comment}")

    return res


def save_comments(levels: LevelsDict, outfilename: str) -> None:
    with open(outfilename, "w") as outfile:
        for level in sorted(levels, reverse=True):
            print("Comments, level", level, file=outfile)
            print(file=outfile)

            for comment in levels[level]:
                print(comment, file=outfile)

            print(file=outfile)


def pdfcomments(infilename: str, outfilename: str = None) -> None:
    levels = load_comments(infilename)

    if outfilename is None:
        outfilename = extsep.join([Path(infilename).namebase, OUT_EXT])

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
