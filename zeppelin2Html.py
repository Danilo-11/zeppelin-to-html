import codecs
import json
import pathlib

import click
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonConsoleLexer
from pygments.lexers import get_lexer_by_name


@click.command()
@click.argument('zeppelin_file', type=click.Path(exists=True))
def convert(zeppelin_file):
    click.echo('Converting Zeppelin file: %s to HTML' % (zeppelin_file))

    with codecs.open(zeppelin_file, 'r', 'utf-8-sig') as z:
        d_zeppelin = json.load(z)
        formatter = HtmlFormatter(full=True)
        html = ['<link rel="stylesheet" type="text/css" href="style.css">']
        for d_para in d_zeppelin['paragraphs']:
            # click.echo(d_para['id'])
            html.extend(para2Html(formatter, d_para))

        input_file = pathlib.Path(zeppelin_file)
        parent_dir = input_file.parent
        html_file = pathlib.Path(parent_dir, input_file.stem + '.html')
        with open(html_file, 'w') as f:
            f.write("\n".join(html))

        click.echo('Html file: %s' % html_file)


def para2Html(formatter, d_para):
    html = []
    if d_para['text']:
        lang = d_para.get('config', {}).get('editorSetting', {}).get('language', 'text')
        l_d_msg = d_para.get('results', {}).get('msg', [])
        if lang == 'markdown':
            html.extend([d_msg['data'] for d_msg in l_d_msg])
        else:
            html.append(highlight(d_para['text'], get_lexer_by_name(lang, stripall=True), formatter))
            for (data, data_type) in map(lambda d_msg: (d_msg['data'], d_msg['type']), l_d_msg):
                if data:
                    if data_type == 'HTML':
                        html.append(data)
                    else:
                        html.append(highlight(data, PythonConsoleLexer(), formatter))
    return html


if __name__ == '__main__':
    convert()
