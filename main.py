import os
import re
from datetime import date
from pathlib import Path

import click
import frontmatter
from emoji import get_emoji_regexp


def emojify(string):
    """
    Find emojis in a string and replace them with an
    inline Markdown image to Twemoji.

    Handles multi-character emojis like flags (🇫🇷 = Ⓕ + Ⓡ)
    """
    def replace(match):
        def codepoint(codes):
            # See https://github.com/twitter/twemoji/issues/419#issuecomment-637360325
            if '200d' not in codes:
                return '-'.join([c for c in codes if c != 'fe0f'])
            return '-'.join(codes)
        cdn_fmt = "https://twemoji.maxcdn.com/v/latest/72x72/{codepoint}.png"
        # {:x} gives hex
        url = cdn_fmt.format(
            codepoint=codepoint([f'{ord(c):x}' for c in match.group(0)])
        )
        return f'!["Emoji"]({url}){{width=16 height=16}}'

    return get_emoji_regexp().sub(replace, string)


def clean_lines(lines):
    res = list(lines)

    pattern = re.compile(r'^::: (tip|warning|danger|lexique)(.*)')

    for i, line in enumerate(lines):
        res[i] = emojify(line)

        # Replace VuePress custom containers
        # https://vuepress.vuejs.org/guide/markdown.html#custom-containers
        m = pattern.match(line.strip())
        if m:
            type, title = [e.strip() for e in m.groups()]
            if type == 'lexique':
                title = f"Lexique : {title}"
            res[i] = f"<div class='banner {type}'>\n**{title}**\n\n"

        if line.strip() == ':::':
            res[i] = '</div>\n'

        # Remove VuePress table of contents
        if line.strip() == '[[toc]]':
            res[i] = ''

    return res


def build_metadata(title):
    date_str = date.today().strftime("%d/%m/%Y")

    return {
        # https://github.com/chdemko/pandoc-latex-environment
        'pandoc-latex-environment': {
            'tip': ['banner', 'tip'],
            'warning': ['banner', 'warning'],
            'danger': ['banner', 'danger'],
            'lexique': ['banner', 'lexique'],
        },
        # https://github.com/Wandmalfarbe/pandoc-latex-template
        'titlepage': "true",
        'toc-own-page': "true",
        'titlepage-color': "FFFFFF",
        'titlepage-text-color': "0053b3",
        'lang': "fr",
        'title': title,
        'author': "Etalab",
        'date': date_str,
        'footer-center': '\small Consultez la dernière version de ce guide sur guides.etalab.gouv.fr',
        'logo': 'logo.png',
        'colorlinks': "true",
        'linkcolor': "etalab-blue",
        'urlcolor': "etalab-blue",
        'numbersections': 'true',
    }


def file_content(f):
    md_content = frontmatter.load(f).content
    lines = f"\n{md_content}\n".split('\n')
    return [f"{l}\n" for l in lines]


@click.command()
@click.argument('folder', type=click.Path(exists=True))
@click.argument('title')
@click.argument('output_path')
def main(folder, title, output_path):
    p = Path(folder)

    # Read Markdown content
    files = [p / 'README.md'] + sorted(list(p.glob('[0-9]*.md')))

    if Path('./images').exists():
        raise ValueError("images folder already exists. Should not exist for symlinks")

    if len(files) < 2:
        raise ValueError(f"Did not find Markdown files in {str(p)}")

    lines = []
    for file in files:
        with file.open() as f:
            lines.extend(file_content(f))

    # Create a single file with all content
    metadata = build_metadata(title)
    content = frontmatter.Post(''.join(clean_lines(lines)), **metadata)
    with open('tmp.md', 'w') as f:
        f.writelines(frontmatter.dumps(content))

    # Build PDF with Pandoc
    os.makedirs(Path(output_path).parent, exist_ok=True)

    os.symlink(p / 'images/', Path('./images'))
    # See https://pandoc.org/MANUAL.html
    # especially "Markdown variants"
    os.system(f'''
    pandoc --toc -s tmp.md -o {output_path} \
      --template "eisvogel.latex" \
      --from markdown+lists_without_preceding_blankline \
      --filter pandoc-latex-environment
    ''')

    # Clean up
    os.unlink(Path('./images'))
    os.remove('tmp.md')

    click.echo(f"PDF file has been generated at {output_path}")

if __name__ == '__main__':
    main()
