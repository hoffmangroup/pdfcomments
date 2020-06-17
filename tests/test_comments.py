from pathlib import Path

from PyPDF2 import PdfFileReader

from pdfcomments.__main__ import load_comments

ROOT = Path(__file__).resolve().parent
PDFS = ROOT / "resources"
assert len(list(PDFS.rglob("*.pdf"))) > 0, "No files in resources directory"


def test_unannotated():
    input_file = PDFS / "unannotated.pdf"
    res = load_comments(PdfFileReader(str(input_file)))
    comments = sum(len(v) for _, v in res.items())
    assert comments == 0


def test_acrobat_comment():
    input_file = PDFS / "annotated_acrobat.pdf"
    res = load_comments(PdfFileReader(str(input_file)))
    comments = sum(len(v) for _, v in res.items())
    assert comments == 1


def test_acrobat_sticky():
    input_file = PDFS / "annotated_acrobat_sticky.pdf"
    res = load_comments(PdfFileReader(str(input_file)))
    comments = sum(len(v) for _, v in res.items())
    assert comments == 1


def test_preview_comment():
    input_file = PDFS / "annotated_preview.pdf"
    res = load_comments(PdfFileReader(str(input_file)))
    comments = sum(len(v) for _, v in res.items())
    assert comments == 1


def test_preview_sticky():
    input_file = PDFS / "annotated_preview_sticky.pdf"
    res = load_comments(PdfFileReader(str(input_file)))
    comments = sum(len(v) for _, v in res.items())
    assert comments == 1


def test_emoji():
    input_file = PDFS / "annotated_emoji.pdf"
    res = load_comments(PdfFileReader(str(input_file)))
    comments = sum(len(v) for _, v in res.items())
    assert comments == 1


def test_underline():
    input_file = PDFS / "annotated_underline.pdf"
    res = load_comments(PdfFileReader(str(input_file)))
    comments = sum(len(v) for _, v in res.items())
    assert comments == 1
