from users.service.comment import CommentService
from typing import Any


class TestCommentServiceGetArticleComments:

    def test_when_no_article_comments(self, comment_service: CommentService) -> None:
        assert not comment_service.get_article_comments(1111)

    def test_when_article_comments_exist(self, comment_service: CommentService, comment_dto: dict[str, Any]) -> None:
        assert comment_service.get_article_comments(comment_dto['article_id'])
