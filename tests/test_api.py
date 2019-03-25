import sys
import os

sys.path.insert(0, "autocomplete/")

from autocomplete.determinist_autosuggest import autoSuggestor

from urllib.parse import urlencode
import json


def call( client, path, params):
    url = path + '?' + urlencode(params)
    response = client.get(url)
    return json.loads(response.data.decode('utf-8'))

def test_route(client):
    result = call(client, '/api/suggest', {'q': "ab"})
    assert "abandon de poste" in result
    assert len(result) == 10

    apos_error = ["' " not in r for r in result]
    assert not any(apos_error)
