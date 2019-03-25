import unittest
import sys
import os

from string import ascii_lowercase

sys.path.insert(0, "../autocomplete/")

link_path = "./autocomplete/data/data_processed_test.txt"
real_link_path = "./autocomplete/data/data_processed_clean.txt"
stops_path = "./autocomplete/data/stops.txt"

from autocomplete.determinist_autosuggest import autoSuggestor, load_stops, load_titles

class TestSuggestor(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSuggestor, self).__init__(*args, **kwargs)
        self.test_instance()
    
    def assertHasAttr(self, obj, intendedAttr):
        testBool = hasattr(obj, intendedAttr)
        self.assertTrue(testBool, msg='obj lacking an attribute. obj: %s, intendedAttr: %s' % (obj, intendedAttr))

    def test_instance(self):
        self.auto = autoSuggestor(link_path, stops_path)
        self.assertHasAttr(self.auto, "titles")
        self.assertHasAttr(self.auto, "stops")

        self.assertHasAttr(self.auto, "d") # dictionnary for tree search
        self.assertHasAttr(self.auto, "precount") # precount for short letter sequences

    def test_suggest(self):
        suggestion = self.auto.auto_suggest('a')
        self.assertIsInstance(suggestion, list) # test result is list
        self.assertIsInstance(suggestion[0], tuple) # test first element of results is tuple
        self.assertIsInstance(suggestion[0][0], str) # test suggestion is string
        self.assertIsInstance(suggestion[0][1], int) # test frequency is int
        self.assertGreater(suggestion[0][1], suggestion[1][1]) # test order
    
    def test_suggest_empty(self):
        suggestion = self.auto.auto_suggest('')
        self.assertIsInstance(suggestion, list) # test result is list

    def test_suggest_skip(self):

        suggestion = self.auto.auto_suggest_skip('a')
        self.assertIsInstance(suggestion, list) # test result is list
        self.assertIsInstance(suggestion[0], tuple) # test first element of results is tuple
        self.assertIsInstance(suggestion[0][0], str) # test suggestion is string
        self.assertIsInstance(suggestion[0][1], int) # test frequency is int
        self.assertGreater(suggestion[0][1], suggestion[1][1]) # test order

    def test_suggest_fast(self):

        suggestion = self.auto.auto_suggest_fast('a')
        self.assertIsInstance(suggestion, list) # test result is list
        self.assertIsInstance(suggestion[0], tuple) # test first element of results is tuple
        self.assertIsInstance(suggestion[0][0], str) # test suggestion is string
        self.assertIsInstance(suggestion[0][1], int) # test frequency is int
        self.assertGreater(suggestion[0][1], suggestion[1][1]) # test order
    
    def test_suggest_empty_skip(self):
        suggestion = self.auto.auto_suggest_skip('')
        self.assertIsInstance(suggestion, list) # test result is list


class TestLoader(unittest.TestCase):
    def test_file_presence(self):
        self.assertTrue(os.path.exists(link_path), "query file: {} not found".format(link_path)) # test query list peresence
        self.assertTrue(os.path.exists(real_link_path), "query file: {} not found".format(real_link_path)) # test query list peresence
        self.assertTrue(os.path.exists(stops_path), "stop words file: {} not found".format(stops_path)) # test query list peresence
    
    def test_load(self):
        stops = load_stops(stops_path)
        titles = load_titles(link_path)
        self.assertIsInstance(stops, list)
        self.assertIsInstance(titles, list)

        self.assertIn("à", stops)
        self.assertIn("de", stops)
        self.assertIn("la", stops)


if __name__ == '__main__':
    unittest.main()