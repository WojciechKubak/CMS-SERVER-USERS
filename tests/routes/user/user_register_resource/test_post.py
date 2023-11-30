from flask.testing import Client
from typing import Any


class TestUserRegisterResourcePost:
    resource = '/users/register'

    def test_when_form_validation_error_occurs(self, client: Client) -> None:
        response = client.post(self.resource, json={})
        assert 400 == response.status_code
        assert b'is required' in response.data

    def test_when_user_service_error_occurs(self, client: Client, user_dto: dict[str, Any]) -> None:
        response = client.post(self.resource, json=user_dto)
        assert 400 == response.status_code
        assert b'Username already in use' in response.data

    def test_when_user_registered_sucessfully(self, client: Client, user_dto: dict[str, Any]) -> None:
        new_user_dto = {key: f"new_{val}" for key, val in user_dto.items()}
        response = client.post(self.resource, json=new_user_dto)
        assert 201 == response.status_code
        assert response.json
