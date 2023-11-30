from flask.testing import Client
from typing import Any


class TestUserNameResourceGet:
    resource = '/users'

    def test_when_user_service_error_occurs(self, client: Client) -> None:
        response = client.get(f"{self.resource}/non_existing_username")
        assert 400 == response.status_code
        assert b'User not found' in response.data

    def test_when_user_found_succesfully(self, client: Client, user_model_data: dict[str, Any]) -> None:
        response = client.get(f"{self.resource}/{user_model_data['username']}")
        assert 200 == response.status_code
        assert user_model_data.items() > response.json.items()
