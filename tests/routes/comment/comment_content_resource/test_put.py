from flask.testing import Client
from typing import Any
import pytest


class TestCommentContentResourcePut:
    request_path = '/comments'

    @pytest.fixture(scope='function')
    def comment_id(self, comment_model_data: dict[str, Any]) -> int:
        return comment_model_data['id']

    def test_when_form_validation_error_occurs(self, client: Client) -> None:
        response = client.put(f"{self.request_path}/1111", json={})
        assert 400 == response.status_code
        assert b'This field is required' in response.data

    def test_when_service_error_occurs(self, client: Client, comment_dto: dict[str, Any], comment_id: int) -> None:
        response = client.put(f"{self.request_path}/{comment_id}", json=comment_dto | {'user_id': 1111})
        assert 400 == response.status_code
        assert b'Comment are not the same' in response.data

    def test_when_content_updated_succesfully(
            self,
            client: Client,
            comment_dto: dict[str, Any],
            comment_id: int
    ) -> None:
        response = client.put(f"{self.request_path}/{comment_id}", json=comment_dto)
        assert 200 == response.status_code
        assert comment_dto.items() < response.json.items()
