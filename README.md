# pdfcomments: extract comments from PDF

pdfcomments extracts comments from a PDF and puts them in a text file.
It is most useful for turning text comments and sticky notes into a list of comments with page numbers.

By default all comments are minor.
You can specify a major comment by adding an asterisk at its beginning.

## Example output

Say you have `test.pdf` and you add the following comments with Acrobat Reader, PDFExpert, or your annotation tool of choice:
- page 1: a text comment, `Text is unclear.`
- page 2: a sticky note, `Sticky note.`
- page 2: a text comment, `* Important comment.`

Run `pdfcomments test.pdf` and it will produce the following output file:

```text
Major comments:

p2: Important comment.

Minor comments:

p1: Text is unclear.
p2: Sticky note.
```

## Prerequisites

- Python >=3.6
- PyPDF2 (installed automatically by `pip`)

## Installation

```sh
python -m pip install pdfcomments@https://codeload.github.com/hoffmangroup/pdfcomments/zip/master
```

Replace `python` with whatever command runs a version that is of Python 3.6 or greater.

## Usage

```
usage: pdfcomments [-h] [--version] infile [outfile]

extract comments from PDF

positional arguments:
  infile      input PDF file
  outfile     output text file (default: infile with extension changed to 'txt')

optional arguments:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
```

## License

GNU General Public License v3.

## Support

You are welcome to post issues but no guarantee of support is provided.
Pull requests are welcome.
