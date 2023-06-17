import sys
import re
import html
import glob
import os

from bs4 import BeautifulSoup
from htmldocx import HtmlToDocx
from docx.shared import Pt

class Work(object):

    def __init__(self, file):
        with open(file) as f:
            self.soup = BeautifulSoup(f.read(), 'html.parser')
        self.metadata = self._parse_metadata()

    def get_title(self):
        return self.soup.css.select_one('.meta h1').get_text()

    def get_published(self):
        return self.metadata['Published']

    def get_fandom(self):
        return self.metadata['Fandom']

    def get_short_fandom_name(self):
        # deal with piped names
        short_name = self.metadata['Fandom'].split('|')[-1]
        short_name = re.sub('\((.*?)\)', '', short_name)
        return short_name.strip()

    def get_collections(self):
        return self.metadata.get('Collections')

    def _parse_metadata(self):
        metadata_tags = self.soup.css.select_one('.meta .tags')
        dt = metadata_tags.find_all('dt')
        dd = metadata_tags.find_all('dd')

        if len(dt) != len(dd):
            raise ValueError('Tag list is not even! Is something wrong with the formatting?')

        metadata = {}
        for name, val in zip(dt, dd):
            metadata.update(self._format_metadata(name, val))
        return metadata

    def _format_metadata(self, name_tag, val_tag):
        name = name_tag.get_text()[:-1]
        val = val_tag.get_text().replace("\n", " ").strip()
        # Handle stats block
        if name == 'Stats':
            name = 'Published'
            m = re.search('Published:\s+(\S+)\s', val)
            val = m.group(1)
        return [(name, val)]

    def get_summary_html(self):
        return self.soup.css.select_one('.meta .userstuff')

    def get_notes_html(self):
        notes = self.soup.css.select('.meta .userstuff')
        if len(notes) > 1:
          return notes[1]

    def get_endnotes_html(self):
        return self.soup.css.select_one('#endnotes')

    def get_body_html(self):
        return self.soup.css.select_one('#chapters .userstuff')

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
        work = Work(input_file)
        Converter(HtmlToDocx(), work).convert_work().save(os.path.join(output_dir, os.path.basename(input_file).replace('.html', '.docx')))

