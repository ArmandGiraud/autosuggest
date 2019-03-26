import pytest

@pytest.fixture
def client():
    from autosuggest import main

    main.app.config['TESTING'] = True
    return main.app.test_client()
