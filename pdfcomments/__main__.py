#!/usr/bin/env python
"""__main__.py: extract comments from PDF
"""
# Copyright 2018-2020 Michael M. Hoffman <michael.hoffman@utoronto.ca>

import argparse
from collections import defaultdict
from pathlib import Path
import re
import sys
from typing import DefaultDict, Iterator, List, TextIO

from PyPDF2 import PdfFileReader
from PyPDF2.pdf import PageObject
from PyPDF2.utils import PdfReadError

from pdfcomments._version import __version__

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

STRICT = False

SEVERITY_NAMES = {0: "Minor comments", 1: "Major comments"}

re_stars = re.compile(
    r"""^
    (?P<stars>\**)
    \s*
    (?P<comment>.*)
    $""",
    re.DOTALL | re.VERBOSE,
)


def iter_annot_contents(page: PageObject) -> Iterator[str]:
    if "/Annots" not in page.keys():
        return

    for indirect in page["/Annots"]:
        obj = indirect.getObject()
        if "popup" in obj.get("/Subtype", "").lower():
            continue
        annot = obj.get("/Contents", "")
        if not isinstance(annot, str):
            for enc in ["utf-8", "utf-16"]:
                try:
                    annot = annot.decode(enc)
                except UnicodeDecodeError:
                    continue
                break

        if annot and isinstance(annot, str):
            yield annot


def load_comments(reader: PdfFileReader) -> SeverityDict:
    res: SeverityDict = defaultdict(list)

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


def pdf_file_type(fp: str) -> str:
    fp = Path(fp)
    if not fp.is_file():
        msg = f"{str(fp)!r} is not a file"
        raise argparse.ArgumentTypeError(msg)
    # Cheap check to see if we have a PDF
    # with fp.open("rb") as fh:
    #     if fh.read(5) != b"%PDF-":
    #         msg = f"{str(fp)!r} doesn't appear to be a pdf"
    #         raise argparse.ArgumentTypeError(msg)

    return str(fp)


def get_parser() -> argparse.ArgumentParser:
    description = __doc__.splitlines()[0].partition(": ")[2]
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "infile", help="input PDF file", type=pdf_file_type,
    )
    parser.add_argument(
        "outfile",
        nargs="?",
        help="output text file (default: infile with extension changed to 'txt')",
        default=None,
    )

    version = f"%(prog)s {__version__}"
    parser.add_argument("--version", action="version", version=version)

    return parser


def main(argv: List[str] = None) -> int:
    parser = get_parser()
    args = parser.parse_args(argv)

    if args.outfile is None:
        # This will output the file in the working directory
        args.outfile = str(Path(args.infile).with_suffix(".txt").name)

    try:
        pdf = PdfFileReader(args.infile, STRICT)
    except PdfReadError as e:
        parser.error(e)

    severities = load_comments(pdf)

    save_comments(severities, args.outfile)


if __name__ == "__main__":
    sys.exit(main())
