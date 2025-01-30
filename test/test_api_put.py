import json

from test.conftest import api_client

#тест на редактирование транзакции
class TestTransaction_put:

    def test_put_transaction(self, api_client):
        url = "http://127.0.0.1:5000/transactions/3"
        payload = {
            "sum": 70000,
            "commission": 17,
            "status": "Тестовая_исправленная",
            "user_id": 1
        }

        response = api_client.put(url, json=payload)

        assert response.status_code == 200
        return json.loads(response.content.decode("utf8"))["id"]
