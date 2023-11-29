from users.model.comment import CommentModel
from flask.testing import Client
from typing import Any


class TestAddCommentResourcePost:
    request_path = '/comments/'

    def test_when_form_validation_error_occurs(self, client: Client) -> None:
        response = client.post(self.request_path, json={})
        assert 400 == response.status_code
        assert b'This field is required' in response.data

    def test_when_service_error_occurs(self, client: Client, comment_dto: dict[str, Any]) -> None:
        response = client.post(self.request_path, json=comment_dto | {'user_id': 1111})
        assert 400 == response.status_code
        assert b'User not found' in response.data

    def test_when_added_succesfully(self, client: Client, comment_dto: dict[str, Any]) -> None:
        response = client.post(self.request_path, json=comment_dto)
        expected = CommentModel.query.filter_by(id=response.json.get('id')).first().to_json()
        assert 201 == response.status_code
        assert expected == response.json
