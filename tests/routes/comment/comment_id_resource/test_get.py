from flask.testing import Client
from typing import Any


class TestCommentIdResourceGet:
    resource = '/comments'

    def test_when_service_error_occurrs(self, client: Client) -> None:
        response = client.get(f'{self.resource}/11111')
        assert 400 == response.status_code
        assert b'Comment not found' in response.data

    def test_when_comment_found_succesfully(self, client: Client, comment_model_data: dict[str, Any]) -> None:
        comment_id = comment_model_data['id']
        response = client.delete(f'{self.resource}/{comment_id}')
        assert 200 == response.status_code
        assert response.json
