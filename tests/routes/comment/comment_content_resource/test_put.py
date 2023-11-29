from users.model.comment import CommentModel
from flask.testing import Client
from typing import Any
import pytest


class TestCommentContentResourcePut:
    request_path = '/comments'

    @pytest.mark.skip('refactoring')
    def test_when_form_validation_error_occurs(self, client: Client, comment_model_data: dict[str, Any]) -> None:
        response = client.put(f"{self.request_path}/1111", json={})
        assert 400 == response.status_code
        assert b'This field is required' in response.data

    @pytest.mark.skip('refactoring')
    def test_when_service_error_occurs(self, client: Client, comment_model_data: dict[str, Any]) -> None:
        response = client.put(
            f"{self.request_path}/{comment_model_data.pop('id')}",
            json=comment_model_data | {'user_id': 1111})
        assert 400 == response.status_code
        assert b'Comment are not the same' in response.data

    @pytest.mark.skip('refactoring')
    def test_when_added_succesfully(self, client: Client, comment_dto: dict[str, Any]) -> None:
        response = client.put(self.request_path, json=comment_dto)
        expected = CommentModel.query.filter_by(id=response.json.get('id')).first().to_json()
        assert 201 == response.status_code
        assert expected == response.json
