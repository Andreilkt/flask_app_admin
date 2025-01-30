import pytest
from conftest import api_client


class TestTransaction:

    def test_get_transaction(self, api_client):
        url = "http://127.0.0.1:5000/transactions/1"
        response = api_client.get(url)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "Создана"
