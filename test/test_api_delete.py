from test.conftest import api_client

#тест на удаление транзакции
class TestTransaction_delete:

    def test_delete_transaction(self, api_client):
        url = "http://127.0.0.1:5000/transactions/3"

        response = api_client.delete(url)

        assert response.status_code == 204
