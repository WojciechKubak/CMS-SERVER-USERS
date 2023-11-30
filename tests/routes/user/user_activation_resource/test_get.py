import pytest

from users.model.user import UserModel
from flask.testing import Client
from datetime import datetime
from typing import Any
import os


class TestUserActivationResourceGet:
    resource = '/users/activate'
    token_lifespan = int(os.getenv('REGISTER_TOKEN_LIFESPAN'))

    @pytest.fixture(scope='session')
    def user_model_id(self, user_model_data: dict[str, Any]) -> int:
        return user_model_data['id']

    def test_when_activation_link_expired(self, client: Client, user_model_id: int) -> None:
        request_data = {
            'timestamp': datetime.utcnow().timestamp() * 1000 - 1,
            'id': user_model_id
        }
        response = client.get(self.resource, query_string=request_data)
        assert 400 == response.status_code
        assert b'Activation link expired' in response.data

    def test_when_user_service_occurs(self, client: Client) -> None:
        request_data = {
            'timestamp': datetime.utcnow().timestamp() * 1000 + self.token_lifespan,
            'id': 11111
        }
        response = client.get(self.resource, query_string=request_data)
        assert b'User not found' in response.data

    def test_when_user_activated_successfully(self, client: Client, user_model_id: int) -> None:
        request_data = {
            'timestamp': datetime.utcnow().timestamp() * 1000 + self.token_lifespan,
            'id': user_model_id
        }
        response = client.get(self.resource, query_string=request_data)
        assert b'User activated' in response.data
        assert UserModel.query.filter_by(id=user_model_id).first().is_active
