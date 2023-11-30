from flask.testing import Client
from typing import Any


class TestUserIdResourceGet:
    resource = '/users'

    def test_when_user_sevice_error_occurs(self, client: Client) -> None:
        response = client.get(f'{self.resource}/11111')
        assert 400 == response.status_code
        assert b'User not found' in response.data

    def test_when_user_found_succesfully(self, client: Client, user_model_data: dict[str, Any]) -> None:
        comment_id = user_model_data['id']
        response = client.get(f'{self.resource}/{comment_id}')
        assert 200 == response.status_code
        assert response.json.items() < user_model_data.items()
