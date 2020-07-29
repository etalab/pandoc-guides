# PDF export for guides with Pandoc

Export [guides](https://github.com/etalab/guides.etalab.gouv.fr) from guides.etalab.gouv.fr to PDF.

## Example

See [example.pdf](example.pdf).

## Installation

Install [pandoc](https://pandoc.org) + [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html). Requires Python 3.8

## Usage

For now, run this code in the folder you want to export as PDF.

```sh
python3 main.py
pandoc --toc -t html5 -V papersize=A4 --css=style.css -s guide.md -o guide.pdf
rm guide.md
```
