import unittest
import sys
import os

# from string import ascii_lowercase

sys.path.insert(0, "../autosuggest/")

link_path = "./autosuggest/data/data_processed_test.txt"
real_link_path = "./autosuggest/data/data_processed_fixed.txt"
content_path = "./autosuggest/data/content.txt"
stops_path = "./autosuggest/data/stops.txt"

from autosuggest.determinist_autosuggest import AutoSuggestor, load_stops, load_queries, load_content


class TestSuggestor(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSuggestor, self).__init__(*args, **kwargs)
        self.test_instance()
    
    def assertHasAttr(self, obj, intendedAttr):
        testBool = hasattr(obj, intendedAttr)
        self.assertTrue(testBool, msg='obj lacking an attribute. obj: %s, intendedAttr: %s' % (obj, intendedAttr))

    def test_instance(self):
        self.auto = AutoSuggestor(link_path, stops_path, content_path)
        self.assertHasAttr(self.auto, "queries")
        self.assertHasAttr(self.auto, "stops")
        self.assertHasAttr(self.auto, "content")

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
    
    def test_suggest_content_empty(self):
        suggestion =  self.auto.suggest_content('')
        self.assertIsInstance(suggestion, list)
        self.assertEqual(suggestion, []) # test that without prefix the suggester does not return results
    
    def test_suggest_content(self):
        # test suggestions is the same for upper and lowercase
        suggestion_u =  self.auto.suggest_content('Horaires')
        suggestion_l = self.auto.suggest_content('horaires')

        self.assertEqual(suggestion_l, suggestion_u)

        # test the number of results equals the parameter given
        n=5
        suggestion_n = self.auto.suggest_content('horaires', n=n)
        self.assertEqual(len(suggestion_n), n)

        # test 

        



class TestLoader(unittest.TestCase):
    def test_file_presence(self):
        self.assertTrue(os.path.exists(link_path), "query file: {} not found".format(link_path)) # test query list presence
        self.assertTrue(os.path.exists(stops_path), "stop words file: {} not found".format(stops_path)) # test query list presence
    
    def test_load(self):
        stops = load_stops(stops_path)
        titles = load_queries(link_path)
        content = load_content(content_path)
        self.assertTrue(len(stops)>0)
        self.assertTrue(len(titles)>0)
        self.assertTrue(len(content)>0)

        self.assertIsInstance(stops, list)
        self.assertIsInstance(titles, list)
        self.assertIsInstance(content, list)
        
        # assert few main stopwords
        self.assertIn("à", stops)
        self.assertIn("de", stops)
        self.assertIn("la", stops)


if __name__ == '__main__':
    unittest.main()
