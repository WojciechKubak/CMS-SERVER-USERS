from users.service.comment import CommentService
from typing import Any
import pytest


class TestCommentServiceGetArticleComments:

    def test_when_user_id_not_found(self, comment_service: CommentService) -> None:
        with pytest.raises(ValueError) as e:
            comment_service.get_user_comments(1111)
        assert 'User not found' == str(e.value)

    def test_when_article_comments_exist(
            self,
            comment_service: CommentService,
            comment_model_data: dict[str, Any]
    ) -> None:
        assert comment_service.get_article_comments(comment_model_data['user_id'])
