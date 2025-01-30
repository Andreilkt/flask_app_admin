import json
from test.conftest import api_client

#тест на добавление транзакции
class TestTransaction_post:

    def test_post_transaction(self, api_client):
        url = "http://127.0.0.1:5000/transactions/"
        payload = {
            "sum": 20001,
            "commission": 11,
            "status": "Тестовая_1",
            "user_id": 1
        }

        response = api_client.post(url, json=payload)

        assert response.status_code == 201
        return json.loads(response.content.decode("utf8"))["id"]







# def test_post_transaction():
#     url = "http://127.0.0.1:5000/transactions/"
#     payload = {
#         "id": 7,
#         "sum": 20000,
#         "commission": 10,
#         "status": "Тестовая",
#         "user_id": 1
#     }
#
#     response = api_client.post(url, json=payload)
#
#     assert response.status_code == 201
#     # return json.loads(response.content.decode("utf8"))["id"]
#
#
#
# def test_post_transaction():
#     url = "http://127.0.0.1:5000/transactions/"
#     data = {
#         "sum": 20000,
#         "commission": 10,
#         "status": "Тестовая",
#         "user_id": 1
#     }
#     response = requests.post(url, json=data)
#
#     assert response.status_code == 201
