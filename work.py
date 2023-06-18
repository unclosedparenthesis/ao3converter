import re

from bs4 import BeautifulSoup

class Work(object):
    """A work from AO3."""

    def __init__(self, file):
        """
        Creates a Work from an AO3-exported HTML file.

        file should be an AO3-generated HTML file (downloaded either via the
        downloads page or via AO3 downloader.
        """
        with open(file) as f:
            self.soup = BeautifulSoup(f.read(), 'html.parser')
        self.metadata = self._parse_metadata()

    def get_title(self):
        """Returns the title of the work, as a string."""
        return self.soup.css.select_one('.meta h1').get_text()

    def get_published(self):
        """Returns the publication date, as a string."""
        return self.metadata['Published']

    def get_fandom(self):
        """Returns the fandom."""
        return self.metadata['Fandom']

    def get_short_fandom_name(self):
        """Returns a shortened version of the fandom name.

        If there are pipes (e.g. 原神 | Genshin Impact (Video Game)), this will pick the last piped name.
        This will also strip parentheses, e.g. (TV).
        """
        # deal with piped names
        short_name = self.metadata['Fandom'].split('|')[-1]
        short_name = re.sub('\((.*?)\)', '', short_name)
        return short_name.strip()

    def get_collections(self):
        """Returns all collections associated with the work, as a comma-separated string."""
        # TODO: This should really be a list.
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
        """Returns the summary as HTML."""
        return self.soup.css.select_one('.meta .userstuff')

    def get_notes_html(self):
        """Returns the preface notes of the work as HTML."""
        notes = self.soup.css.select('.meta .userstuff')
        if len(notes) > 1:
          return notes[1]

    def get_endnotes_html(self):
        """Returns endnotes as an HTML tag."""
        return self.soup.css.select_one('#endnotes')

    def get_body_html(self):
        """Returns the body of a work as an HTML tag."""
        return self.soup.css.select_one('#chapters .userstuff')
