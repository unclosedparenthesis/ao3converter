"""
Converts AO3-formatted files into DOCX.

Usage:
    python3 docx_converter.py [input directory] [output directory]

Output directory must already exist.
"""

import sys
import re
import html
import glob
import os
import work

from bs4 import BeautifulSoup
from htmldocx import HtmlToDocx
from docx.shared import Pt


class Converter(object):

    def __init__(self, parser, work):
        self.work  = work
        self.parser = parser

    def convert_work(self):
        html_str = []
        html_str.append("""
<html>
<body>
<h1>{title}</h1>
<br/>
{summary}<p/>
""".format(title=html.escape(self.work.get_title()), summary=self.work.get_summary_html()))

        metadata_tuples = [
                ('Fandom:', self.work.get_short_fandom_name()),
                ('Originally Published:', self.work.get_published()),
                ('Collections:', self.work.get_collections())
                ]
        metadata = ["<tr><td>{}<td/><td>{}<td/></tr>".format(html.escape(x), html.escape(y)) for x, y in metadata_tuples if y]
        html_str.append("<table>{}</table>".format('\n'.join(metadata)))

        notes = self.work.get_notes_html()
        if notes:
            html_str.append("<p>Notes:</p>{}<hr/>".format(notes))

        html_str.append(str(self.work.get_body_html()))

        endnotes = self.work.get_endnotes_html()
        if endnotes:
            html_str.append("<p /p></p><p>Afterword:</p> {}".format(endnotes))
        html_str.append("</body></html>")

        doc = self.parser.parse_html_string(''.join(html_str))
        style = doc.styles['Normal']
        font = style.font
        font.name = 'Arial'
        font.size = Pt(11)
        return doc


if __name__ == '__main__':
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    for input_file in glob.glob(os.path.join(input_dir, '*.html')):
        w = work.Work(input_file)
        Converter(HtmlToDocx(), w).convert_work().save(os.path.join(output_dir, os.path.basename(input_file).replace('.html', '.docx')))

