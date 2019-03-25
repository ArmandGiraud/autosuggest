from .determinist_autosuggest import AutoSuggestor
from .download import maybe_download_queries


def autosuggest(prefix=None, url=None, stops_path=None, queries_paths=None, **kw):
    queries_paths = maybe_download_queries(queries_paths, url=url, overwrite=kw.pop('overwrite', False))
    auto = AutoSuggestor(queries_paths, stops_path, build_precount=prefix is not None)

    if prefix is None:
        return auto
    else:
        return auto.auto_suggest_fast(prefix, **kw)
