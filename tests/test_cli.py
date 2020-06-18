import io
from pathlib import Path
import sys
import tempfile
import unittest

from PyPDF2 import PdfFileReader, PdfFileWriter

from pdfcomments.__main__ import get_parser, main, __version__


ROOT = Path(__file__).resolve().parent
PDFS = ROOT / "resources"
assert len(list(PDFS.rglob("*.pdf"))) > 0, "No files in resources directory"


class TestProg(unittest.TestCase):
    def setUp(self) -> None:
        # Create temp directory
        self._dir = tempfile.TemporaryDirectory()
        self.test_dir = self._dir.name

        # Open pdf that has annotations
        pdf = PDFS / "annotated_acrobat.pdf"
        pdf = PdfFileReader(pdf.open("rb"))

        # Create temp pdf file in directory
        out = PdfFileWriter()
        out.addBlankPage(612, 792)
        out.appendPagesFromReader(pdf)

        self.test_pdf = f"{self.test_dir}/temp.pdf"
        with open(self.test_pdf, "wb") as fh:
            out.write(fh)
        # Construct best guess at output
        self.expected_out = """Minor comments:

p2: Is this about bioinformaticians?

"""

    def tearDown(self) -> None:
        # Delete temp directory
        self._dir.cleanup()

    def test_write_to_location(self):
        output = f"{self.test_dir}/out.txt"
        opts = [self.test_pdf, output]
        main(opts)
        file_contents = open(output, "r").read()
        self.assertEqual(self.expected_out, file_contents)

    def test_write_to_cwd(self):
        output = Path(self.test_pdf).with_suffix(".txt").name
        opts = [self.test_pdf]
        main(opts)
        file_contents = open(output, "r").read()
        self.assertEqual(self.expected_out, file_contents)


class TestCLI(unittest.TestCase):
    def setUp(self) -> None:
        self.out, self.err = io.StringIO(), io.StringIO()
        self._out, self._err = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = self.out, self.err

    def tearDown(self) -> None:
        sys.stdout, sys.stderr = self._out, self._err

    def test_version(self):
        with self.assertRaises(SystemExit):
            main(["--version"])

        self.out.seek(0)
        version_line = self.out.readline().strip()
        self.assertTrue(version_line.endswith(__version__))

    def test_not_a_file(self):
        opts = ["not_a_real_file.pdf"]
        with self.assertRaises(SystemExit):
            main(opts)

        self.err.seek(0)
        err = self.err.read().strip()
        self.assertTrue(
            err.endswith("error: argument infile: 'not_a_real_file.pdf' is not a file")
        )

    def test_not_a_pdf(self):
        err_strs = (
            "error: EOF marker not found",
            "error: Could not read malformed PDF file",
        )
        opts = [__file__]
        with self.assertRaises(SystemExit):
            main(opts)

        self.err.seek(0)
        err = self.err.read().strip()
        self.assertTrue(any(err.endswith(s) for s in err_strs))

    def test_encrypted(self):
        opts = [str(PDFS / "annotated_acrobat_encrypted.pdf")]
        with self.assertRaises(SystemExit):
            main(opts)

        self.err.seek(0)
        err = self.err.read().strip()
        self.assertTrue(err.endswith("Encrypted PDFs are currently unsupported"))


if __name__ == '__main__':
    unittest.main()
