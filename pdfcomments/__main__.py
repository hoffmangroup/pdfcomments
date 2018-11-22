#!/usr/bin/env python
"""__init__.py: extract comments from PDF
"""

__version__ = "0.1"

# Copyright 2018 Michael M. Hoffman <michael.hoffman@utoronto.ca>

from argparse import Namespace
from os import extsep
from re import compile as re_compile, DOTALL, escape, MULTILINE
from subprocess import run
import sys
from typing import List, Optional

from path import Path
from pkg_resources import resource_filename

ENCODING = "utf-8"
STYLESHEET_RESOURCENAME = "data/pdfcomments.xsl"
OUT_EXT = "txt"

pattern_encoded_xhtml_start = escape(r"&lt;?xml version='1.0'?&gt;&lt;body xmlns='http://www.w3.org/1999/xhtml' xmlns:xfa='http://www.xfa.org/schema/xfa-data/1.0/' xfa:APIVersion='Acrobat:10.1.2' xfa:spec='2.0.2'&gt;&lt;p dir='ltr' style='color: #ff0000'&gt;&lt;span&gt;")  # noqa
pattern_encoded_xhtml_end = escape(r"&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;")

pattern_encoded_xhtml = \
    f"{pattern_encoded_xhtml_start}(.*?){pattern_encoded_xhtml_end}"
re_encoded_xhtml = re_compile(pattern_encoded_xhtml, MULTILINE | DOTALL)

re_squo = re_compile(r"&amp;[lr]squo;")
re_dquo = re_compile(r"&amp;[lr]dquo;")


def pdfcomments(infilename: str, outfilename: str = None):
    if outfilename is None:
        outfilename = extsep.join([Path(infilename).namebase, OUT_EXT])

    with open(infilename) as infile:
        text = infile.read()

    text_clean = re_encoded_xhtml.sub(r"\1", text)
    text_clean = re_squo.sub("'", text_clean)
    text_clean = re_dquo.sub('"', text_clean)

    bytes_clean = text_clean.encode(ENCODING)

    stylesheet_filename = resource_filename(__name__, STYLESHEET_RESOURCENAME)
    run(["xsltproc", "-o", outfilename, stylesheet_filename, "-"],
        input=bytes_clean, check=True)


def parse_args(args: List[str]) -> Namespace:
    from argparse import ArgumentParser

    description = __doc__.splitlines()[0].partition(": ")[2]
    parser = ArgumentParser(description=description)
    parser.add_argument("infile", help="input file in xfdf format")
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
