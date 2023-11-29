from users.service.comment import CommentService
from users.model.comment import CommentModel
from typing import Any
import pytest


class TestCommentServiceGetCommentById:

    def test_when_comment_id_not_found(self, comment_service: CommentService) -> None:
        with pytest.raises(ValueError) as e:
            comment_service.get_comment_by_id(1111)
        assert 'Comment not found' == str(e.value)

    def test_when_comment_found_succesfully(
            self,
            comment_service: CommentService,
            comment_model_data: dict[str, Any]
    ) -> None:
        result = comment_service.get_comment_by_id(comment_model_data['id'])
        assert CommentModel.query.filter_by(id=result.id).first() == result
