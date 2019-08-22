from .determinist_autosuggest import AutoSuggestor
from .download import maybe_download_queries


def autosuggest(prefix=None, url=None, stops_path=None, queries_path=None, **kw):
    """convenience function to avoid download data"""
    queries_path = maybe_download_queries(queries_path, url=url, overwrite=kw.pop('overwrite', False))
    auto = AutoSuggestor(queries_path, stops_path, build_precount=prefix is not None)

    if prefix is None:
        return auto
    else:
        return auto.auto_suggest_fast(prefix, **kw)
