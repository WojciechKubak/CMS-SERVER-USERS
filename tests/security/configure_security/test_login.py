from users.model.user import UserModel
from unittest.mock import patch, PropertyMock
from flask.testing import Client
from typing import Any
import pytest


class TestConfigureSecurityLogin:
    request_path = '/login'

    @pytest.fixture(scope='session')
    def login_data(self, user_dto: dict[str, Any]) -> dict[str, Any]:
        return {
            'username': user_dto['username'],
            'password': user_dto['password']
        }

    def test_when_user_does_not_exist(self, client: Client, login_data: dict[str, Any]) -> None:
        response = client.post(
            self.request_path,
            json={"username": f"{login_data['username']}11", 'password': login_data['password']})

        assert 401 == response.status_code
        assert b'User not found' in response.data

    def test_when_password_is_incorrect(self, client: Client, login_data: dict[str, Any]) -> None:
        response = client.post(
            self.request_path,
            json={"username": f"{login_data['username']}", 'password': f"{login_data['username']}11"})

        assert 401 == response.status_code
        assert b'Incorrect password' in response.data

    def test_when_user_is_not_active(self, client: Client, login_data: dict[str, Any]) -> None:
        response = client.post(self.request_path, json=login_data)

        assert 401 == response.status_code
        assert b'User is not activated' in response.data

    def test_when_logged_in_succesfully(self, client: Client, login_data: dict[str, Any]) -> None:
        with patch.object(UserModel, 'is_active', new_callable=PropertyMock) as attr_mock:
            attr_mock.return_value = True
            response = client.post(self.request_path, json=login_data)

        assert 200 == response.status_code
        assert b'Login successful' in response.data
        assert 'access_token_cookie' in response.headers['Set-Cookie']
