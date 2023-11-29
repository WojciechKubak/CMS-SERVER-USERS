from users.service.comment import CommentService
from users.model.comment import CommentModel
from typing import Any
import pytest


class TestCommentServiceGetArticleComments:

    def test_when_comment_id_not_found(
            self,
            comment_service: CommentService,
            comment_model_data: dict[str, Any]
    ) -> None:
        with pytest.raises(ValueError) as e:
            comment_service.update_comment_content(comment_model_data | {'id': 1111})
        assert 'Comment not found' in str(e.value)

    def test_when_comments_are_not_equal(
            self,
            comment_service: CommentService,
            comment_model_data: dict[str, Any]
    ) -> None:
        with pytest.raises(ValueError) as e:
            comment_service.update_comment_content(comment_model_data | {'user_id': 1111})
        assert 'Comment are not the same' in str(e.value)

    def test_when_updated_succesfully(
            self,
            comment_service: CommentService,
            comment_model_data: dict[str, Any]
    ) -> None:
        result = comment_service.update_comment_content(comment_model_data | {'content': 'new content'})
        assert CommentModel.query.filter_by(id=comment_model_data['id']).first() == result
