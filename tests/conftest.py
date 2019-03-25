import pytest

@pytest.fixture
def client():
    from autocomplete import main

    main.app.config['TESTING'] = True
    return main.app.test_client()