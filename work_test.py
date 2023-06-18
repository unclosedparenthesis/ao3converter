import unittest
import work

class WorkTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.work = work.Work('test_work.html')

    def test_get_title(self):
        self.assertEqual(self.__class__.work.get_title(), "Title")

    def test_get_published(self):
        self.assertEqual('2001-01-01', self.__class__.work.get_published())

    def test_get_fanhom(self):
        self.assertEqual('Fandom', self.__class__.work.get_fandom())

    def test_get_collection(self):
        self.assertEqual('Collection Name', self.__class__.work.get_collections())

    def test_get_body_html(self):
        self.assertEqual(self.__class__.work.get_body_html().get_text(strip=True), "A fic!Even more things in the fic!")

    def test_get_endnotes_html(self):
        self.assertEqual(self.__class__.work.get_endnotes_html().get_text(strip=True), "End NotesEnd note")

if __name__ == '__main__':
    unittest.main()

