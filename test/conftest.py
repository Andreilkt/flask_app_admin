import pytest
import requests


@pytest.fixture(scope="function")
def api_client():
    return requests.Session()