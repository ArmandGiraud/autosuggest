"""utilities to check data, annd download it"""

import urllib.request as urllib
from pathlib import Path

from .resources import get_resource


def maybe_download_queries(path=None, url=None, overwrite: bool = False):
    if path is None:
        path = 'queries.txt'

    path = Path(path).expanduser()

    if overwrite and url is not None:
        if path.is_file():
            print(f"Downloading '{url}' and overwriting to '{path}'...")
        else:
            print(f"Downloading '{url}' to '{path}'...")
        file_path, _ = urllib.urlretrieve(url=url, filename=path)
        return path

    if path.is_file():
        print(f'using existing file: "{path.absolute()}"')
        return path

    _path = get_resource(str(path))
    if not _path.is_file():
        assert url is not None, "you must provide a valid URL to download the queries"
        path = Path.cwd() / path
        print(f"Downloading '{url}' to '{path}'...")
        file_path, _ = urllib.urlretrieve(url=url, filename=path)
        return path
    else:
        print(f"using package's default test file \"{_path}\"")
        path = _path
        return path
