#!/usr/bin/env python
"""__init__.py: extract comments from PDF
"""

__version__ = "0.1"

# Copyright 2018, 2019 Michael M. Hoffman <michael.hoffman@utoronto.ca>

from argparse import Namespace
from collections import OrderedDict
from os import extsep
import sys
from typing import List, Optional

from path import Path

from PyPDF2 import PdfFileReader

ENCODING = "utf-8"  # XXX: still used?
OUT_EXT = "txt"
STRICT = False

# XXX: still used?
REPLACEMENTS = OrderedDict([(r"&amp;[lr]squo;", "'"),
                            (r"&amp;[lr]dquo;", '"'),
                            (r"&amp;gt;", ">"),
                            (r"&amp;lt;", "<")])


def pdfcomments(infilename: str, outfilename: str = None):
    if outfilename is None:
        outfilename = extsep.join([Path(infilename).namebase, OUT_EXT])

    reader = PdfFileReader(infilename, STRICT)
    for page_num, page in enumerate(reader.pages):
        page_text = f"p{page_num+1}:"

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

            print(page_text, contents)
            # XXX: open outputfile, print there


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
