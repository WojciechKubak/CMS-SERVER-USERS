from users.model.comment import CommentModel
from flask.testing import Client
from typing import Any


class TestCommentUserIdResourceGet:
    resource = '/comments/user'

    def test_when_service_error_occurs(self, client: Client) -> None:
        response = client.get(f'{self.resource}/1111')
        assert 400 == response.status_code
        assert b'User not found' in response.data

    def test_when_data_found_succesfully(self, client: Client, user_model_data: dict[str, Any]) -> None:
        user_id = user_model_data['id']
        response = client.get(f'{self.resource}/{user_id}')
        assert 200 == response.status_code
        assert len(CommentModel.query.filter_by(user_id=user_id).all()) == len(response.json)
