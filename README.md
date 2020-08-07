# PDF export for guides with Pandoc

Export [guides](https://github.com/etalab/guides.etalab.gouv.fr) from guides.etalab.gouv.fr to PDF.

## Example

See [example.pdf](example.pdf).

## Installation

Install [pandoc](https://pandoc.org) + LaTeX. You may use a [Docker image](https://hub.docker.com/r/pandoc/latex).

Requires Python 3.8.

## Usage

Clone in the folder where your documentation folders are.

```sh
python3 -m venv venv
source venv/bin/activate
python main.py src "My documentation title" out/document.pdf
```

Arguments are:
- `src_folder`: the folder where Markdown files are;
- `title`: title of the document;
- `output_path`: of the generated PDF file.

## Script details

This repository is a Python CLI. The goal is to aggregate multiple Markdown files in a folder to produce a beautiful PDF.

This script handles:
- collecting multiple Markdown files into a single one;
- converting non-standard Markdown: VuePress table of contents, emojis, custom blocks;
- calling Pandoc with the appropriate options and parameters to produce a beautiful PDF file.
