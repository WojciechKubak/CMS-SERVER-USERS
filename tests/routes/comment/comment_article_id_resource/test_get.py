from flask.testing import Client
from typing import Any


class TestCommentArticleIdResource:
    request_path = '/comments/article'

    def test_when_no_data_found(self, client: Client) -> None:
        response = client.get(f"{self.request_path}/1111")
        assert 200 == response.status_code
        assert not response.json

    def test_when_data_found_succesfully(self, client: Client, comment_dto: dict[str, Any]) -> None:
        response = client.get(f"{self.request_path}/{comment_dto['article_id']}")
        assert 200 == response.status_code
        assert response.json
