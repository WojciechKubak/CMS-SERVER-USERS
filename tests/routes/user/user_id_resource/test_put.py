from flask.testing import Client
from typing import Any
import pytest


class TestUserIdResourcePut:
    request_path = '/users'

    @pytest.fixture(scope='function')
    def user_id(self, user_model_data: dict[str, Any]) -> int:
        return user_model_data['id']

    def test_when_user_service_error_occurs(self, client: Client, user_dto: dict[str, Any]) -> None:
        response = client.put(f"{self.request_path}/11111", json=user_dto)
        assert 400 == response.status_code
        assert b'User not found' in response.data

    def test_when_user_updated_succesfully(self, client: Client, user_dto: dict[str, Any], user_id: int) -> None:
        updated_username = 'new_username'
        response = client.put(f"{self.request_path}/{user_id}", json=user_dto | {'username': updated_username})
        assert 200 == response.status_code
        assert updated_username == response.json['username']
