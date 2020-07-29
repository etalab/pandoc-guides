from pathlib import Path
import re


def replace_lines(lines):
    res = list(lines)

    pattern = re.compile(r'^::: (tip|warning|danger|lexique)(.*)')

    for i, line in enumerate(lines):
        res[i] = line

        # Replace VuePress custom containers
        # https://vuepress.vuejs.org/guide/markdown.html#custom-containers
        m = pattern.match(line.strip())
        if m:
            type, title = [e.strip() for e in m.groups()]
            if type == 'lexique':
                title = f"Lexique : {title}"
            res[i] = f"<div class='banner {type}'><p class='banner-title'>{title}</p>\n"

        if line.strip() == ':::':
            res[i] = '</div>\n'

        # Hack to remove YAML header content
        # Horrible code.
        if line.strip() == '---' or 'permalink:' in line:
            res[i] = '\n'

    return res

p = Path('.')

files = [p / 'README.md'] + sorted(list(p.glob('[0-9]*.md')))

lines = []
for file in files:
    with file.open() as f:
        lines.extend(f.readlines())

with open('guide.md', 'w') as f:
    f.writelines(replace_lines(lines))
