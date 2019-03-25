"""main script for autosuggest"""

import os
from determinist_autosuggest import autoSuggestor
from download import maybe_download

if __name__ == "__main__":
    link_path = "./data/data_processed_fixed.txt"
    stops_path = "./data/stops.txt"

    data_dir = os.path.abspath(os.path.join(__file__, os.pardir))
    stops_path = os.path.join(data_dir, stops_path)
    link_path = os.path.join(data_dir, link_path)
    
    
    maybe_download(url)
    auto = autoSuggestor(link_path, stops_path, build_precount = False)

    prefix  = "con"
    suggestions = auto.auto_suggest_fast(prefix)
    print(suggestions)