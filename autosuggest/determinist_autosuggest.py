from collections import Counter, defaultdict
from pathlib import Path
from itertools import combinations
from string import ascii_lowercase
from typing import List
from random import shuffle

from .resources import get_resource

list_str = List[str] # typing util

DEFAULTS = {
    'queries': 'queries.txt',
    'stops': 'stops.txt',
    'content': 'content.txt'
}

def load_queries(queries_path=None):
    if queries_path is None:
        queries_path = get_resource(DEFAULTS['queries'])
    else:
        queries_path = Path(queries_path).expanduser().resolve()

    return queries_path.read_text(encoding='utf-8').splitlines()


def load_stops(stops_path=None):
    if stops_path is None:
        stops_path = get_resource(DEFAULTS['stops'])
    else:
        stops_path = Path(stops_path).expanduser().resolve()

    return stops_path.read_text(encoding='utf-8').splitlines()

def load_content(content_path=None):
    if content_path is None:
        content_path = get_resource(DEFAULTS["content"])
    else:
        content_path = Path(content_path).expanduser().resolve()

    return content_path.read_text(encoding='utf-8').splitlines()

class AutoSuggestor:
    def __init__(self, queries_path=None,
                       stops_path=None,
                       content_path=None,
                       build_precount: int = 2,
                       pre_hash_maxlen: int = 4):
        self.queries = load_queries(queries_path)
        self.stops = load_stops(stops_path)

        # add content if path is provided

        if content_path is not None:
            content = load_content(content_path)
            shuffle(content)
            self.content = content 
        self.precount = {}
        # defaults to 2 (when `build_precount` is True)
        self._pcl = (2 if build_precount else 0) if isinstance(build_precount, bool) else build_precount

        self.d = defaultdict(list)
        self._phml = None

        self._build_dict(pre_hash_maxlen)
        if build_precount:
            self._init_precount(self._pcl)

    def _build_dict(self, n=4):
        """making a hashtable tree search with the first 4 characters"""
        self._phml = n
        for t in self.queries:
            for i in range(0, n + 1):
                self.d[t[:i]].append(t)
    
    def _request_dict(self, req):
        filtered_dic = self.d[req[:self._phml]]  # use the N number of characters used to build the hashtable
        res = [t for t in filtered_dic if t.startswith(req)]
        return res
    
    def _init_precount(self, precount_length: int = 2):
        """initialise precount of short prefixes for faster execution,
         precomputing takes time at instanciation, but much faster on prediction with some memory overhed
         precount_length is the number of characters involved in precomputation"""
        precount = defaultdict(list)
        letters_prefix = [a + b for a, b in combinations(ascii_lowercase, precount_length)]
        letters_prefix += [a for a in ascii_lowercase]

        for char in letters_prefix:
            precount[char] = self.auto_suggest_skip(char)
        
        self.precount = precount
        self._pcl = precount_length
    
    def auto_suggest(self, pref, n: int = 10, freq_min: int = 2):
        """old version without trailing stopwords"""
        len_pref = len(pref.split())
        suggestions = [t for t in self.queries if t.startswith(pref.lower())]
        most_common = Counter([" ".join(sg.split()[:(len_pref + 2)]) for sg in suggestions]).most_common(n)
        return [(m[0], m[1]) for m in most_common if m[1] > freq_min]

    def auto_suggest_skip(self, pref, n: int = 10, freq_min: int = 5, nb_next_words: int = 2):
        # function to suggest next words in user query, skipping stopwords
        if pref == "":
            return []
        len_pref = len(pref.lower().split())
        suggestions = [t for t in self.queries if t.startswith(pref.lower())]
        suggestions = [sg.split() for sg in suggestions]
        suggest_ = [sg[:(len_pref + nb_next_words + 1)]
                    if sg[:(len_pref + nb_next_words)][-1] in self.stops
                    else sg[:(len_pref + nb_next_words)] for sg in suggestions]
        most_common = Counter([" ".join(sg) for sg in suggest_]).most_common(n)
        return [(m[0], m[1]) for m in most_common if m[1] > freq_min]
    
    def auto_suggest_fast(self, pref, n: int = 10, freq_min: int = 2, nb_next_words: int = 2, return_freq: bool = True):
        """faster version with pre-computing, hashtable research, and trailing stopwords skip"""
        if pref == "":
            return [[], []]
        len_pref = len(pref.split())
        if pref in self.precount.keys():
            return self.precount[pref]
        suggestions = self._request_dict(pref.lower())
        suggestions = [sg.split() for sg in suggestions]
        suggest_ = [sg[:(len_pref + nb_next_words + 1)]
                    if sg[:(len_pref + nb_next_words)][-1] in self.stops
                    else sg[:(len_pref + nb_next_words)] for sg in suggestions]
        most_common = Counter([" ".join(sg) for sg in suggest_]).most_common(n)
        if return_freq:
            return [(m[0], m[1]) for m in most_common if m[1] > freq_min]
        else:
            return [m[0] for m in most_common if m[1] > freq_min]

    def suggest_content(self, prefix: str, n=10):
        """suggest actual website content from a list of documents titles
        args:
        prefix: user prefix in search bar
        title: list of documents titles to suggest from
        n: number of suggestions to return
        return list of string titles"""

        if prefix in ["", " "]:
            return []
        try:
            self.content
        except ValueError:
            print("No content titles were found: check if path was provided")
                
        return [t for t in self.content if prefix.lower() in t.lower()][:n]
        