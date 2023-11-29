from users.model.user import UserModel
from unittest.mock import patch, PropertyMock
from flask.testing import Client


class TestJWTRequiredWithRoles:
    request_path = '/resource'

    def test_when_unauthorized(self, client: Client) -> None:
        response = client.get(self.request_path)
        assert 401 == response.status_code
        assert b'Token is missing or invalid' in response.data

    def test_when_insufficient_permissions(self, client: Client, access_token: str) -> None:
        client.set_cookie('access_token_cookie', access_token)

        response = client.get(self.request_path)

        assert 403 == response.status_code
        assert b'Insufficient permissions' in response.data

    def test_when_authenticated(self, client: Client, access_token: str) -> None:
        with patch.object(UserModel, 'role', new_callable=PropertyMock) as attr_mock:
            attr_mock.return_value = 'admin'

            client.set_cookie('access_token_cookie', access_token)
            response = client.get(self.request_path)

        assert 200 == response.status_code
        assert b'content' in response.data
