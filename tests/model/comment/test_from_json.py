from users.model.comment import CommentModel
from typing import Any


def test_comment_model_from_json(comment_dto: dict[str, Any]) -> None:
    comment = CommentModel.from_json(comment_dto)
    assert comment_dto.items() < comment.__dict__.items()
