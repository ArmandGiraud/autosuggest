import re
import os
from collections import Counter, defaultdict
from itertools import chain

def load_titles(link_path):
    """read default path if data file not given"""
    if not link_path:
        dir_path = os.path.dirname(os.path.abspath(__file__))
        link_path = os.path.join(dir_path, "data/data_processed_fixed.txt")
    with open(link_path, encoding = "utf-8") as f:
        d = f.read().splitlines()
    return d

def load_stops(stops_path):
    """read default path if data file not given"""
    if not stops_path:
        dir_path = os.path.dirname(os.path.abspath(__file__))
        stops_path = os.path.join(dir_path, "data/stops.txt")
    with open(stops_path, encoding = "utf-8") as f:
        stops = f.read().splitlines()
    return stops

class autoSuggestor:
    def __init__(self, link_path1 = None, link_path2 = None, stops_path = None, build_precount = True):
        titles1, titles2 = load_titles(link_path1) , load_titles(link_path1)
        
        self.titles = titles1 + titles2
        self.stops = load_stops(stops_path)
        self._build_dict()

        if build_precount:
            self._init_precount()
        else:
            self.precount = {}

    def _build_dict(self, n = 4):
        """making a hashtable tree search with the first 4 characters"""

        self.d = defaultdict(list)
        for t in self.titles:
            for i in range(0, n + 1):
                self.d[t[:i]].append(t)
    
    def _request_dict(self, req):
        filtered_dic = self.d[req[:4]]
        res = [t for t in filtered_dic if t.startswith(req)]
        return res
    
    def _init_precount(self, precount_length = 2):
        """initialise precount of short prefixes for faster execution,
         precomputing takes time at instanciation, but much faster on prediction with some memory overhed
         precount_length is the number of characters involved in precomputation"""

        from itertools import combinations
        from string import ascii_lowercase

        precount = defaultdict(list)
        letters_prefix = [a + b for a, b in combinations(ascii_lowercase, precount_length)] # 
        letters_prefix += [a for a in ascii_lowercase]

        for char in letters_prefix:
            precount[char] = self.auto_suggest_skip(char)
        
        self.precount = precount
    
    def auto_suggest(self, pref, n = 10, freq_min = 2):
        "old version without trailing stopwords"
        len_pref = len(pref.split())
        suggestions = [t for t in self.titles if t.startswith(pref.lower())]
        most_common = Counter([" ".join(sg.split()[:(len_pref + 2)]) for sg in suggestions]).most_common(n)
        return [(m[0], m[1]) for m in most_common if m[1] > freq_min]

    def auto_suggest_skip(self, pref, n = 10, freq_min = 5, nb_next_words = 2):
        #function to suggest next words in user query, skipping stopwords
        if pref == "":
             return []
        len_pref = len(pref.lower().split())
        suggestions = [t for t in self.titles if t.startswith(pref.lower())]
        suggestions = [sg.split() for sg in suggestions]
        suggest_ = [sg[:(len_pref + nb_next_words + 1)] if sg[:(len_pref + nb_next_words)][-1] in self.stops else sg[:(len_pref + nb_next_words)] for sg in suggestions]
        most_common = Counter([" ".join(sg) for sg in suggest_]).most_common(n)
        return [(m[0], m[1] ) for m in most_common if m[1] > freq_min]
    
    def auto_suggest_fast(self, pref, n = 10, freq_min = 2, nb_next_words = 2, return_freq = True):
        "faster version with precomputing, hastable research, and trailing stopwords skip"
        if pref == "":
             return [[], []]
        len_pref = len(pref.split())
        if pref in self.precount.keys():
            return self.precount[pref]
        suggestions = self._request_dict(pref.lower())
        suggestions = [sg.split() for sg in suggestions]
        suggest_ = [sg[:(len_pref + nb_next_words + 1)] if sg[:(len_pref + nb_next_words)][-1] in self.stops else sg[:(len_pref + nb_next_words)] for sg in suggestions]
        most_common = Counter([" ".join(sg) for sg in suggest_]).most_common(n)
        if return_freq:
            return [(m[0], m[1]) for m in most_common if m[1] > freq_min]
        else:
            return [m[0] for m in most_common if m[1] > freq_min]