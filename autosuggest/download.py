"""utilities to check data, annd download it"""

import urllib.request as urllib
import os

SAVE_PATH = "data/data_processed_fixed.txt"
data_dir = os.path.abspath(os.path.join(__file__, os.pardir))
SAVE_PATH = os.path.join(data_dir, SAVE_PATH)

def maybe_download(url):
    print("Downloading {}".format(os.path.basename(SAVE_PATH)))
    if not os.path.exists(SAVE_PATH):
        file_path, _ = urllib.urlretrieve(url=url,
                                            filename=SAVE_PATH)

if __name__ == "__main__":
    maybe_download(url = "secret url")