from users.service.comment import CommentService
from users.model.comment import CommentModel
from typing import Any
import pytest


class TestCommentServiceDeleteComment:

    def test_when_id_not_found(self, comment_service: CommentService) -> None:
        with pytest.raises(ValueError) as e:
            comment_service.delete_comment(1111)
        assert 'Comment not found' == str(e.value)

    def test_when_deleted_succesfully(
            self,
            comment_service: CommentService,
            comment_model_data: dict[str, Any]
    ) -> None:
        result = comment_service.delete_comment(comment_model_data['id'])
        assert not CommentModel.query.filter_by(id=result).first()
