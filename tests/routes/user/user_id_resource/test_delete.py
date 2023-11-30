from flask.testing import Client
from users.model.user import UserModel
from typing import Any


class TestUserIdResourceDelete:
    resource = '/users'

    def test_when_service_error_occurrs(self, client: Client) -> None:
        response = client.delete(f'{self.resource}/11111')
        assert 400 == response.status_code
        assert b'User not found' in response.data

    def test_when_user_deleted_succesfully(self, client: Client, user_model_data: dict[str, Any]) -> None:
        user_id = user_model_data['id']
        response = client.delete(f'{self.resource}/{user_id}')
        assert 200 == response.status_code
        assert not UserModel.query.filter_by(id=user_id).first()
