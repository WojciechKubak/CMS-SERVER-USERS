from users.model.user import UserModel
from users.model.comment import CommentModel
from users.db.configuration import sa
from flask import Flask
from typing import Callable, Any
import pytest


@pytest.fixture(scope='session')
def comment_model_with_id(comment_model_data: dict[str, Any]) -> Callable[[int], UserModel]:
    def create_model(id_: int) -> UserModel:
        return CommentModel(**comment_model_data | {'id': id_})
    return create_model


@pytest.fixture
def comment_model(comment_model_with_id: Callable[[int], CommentModel]) -> CommentModel:
    return comment_model_with_id(1)


@pytest.fixture(autouse=True)
def add_comment(app: Flask, comment_model: UserModel) -> None:
    sa.session.add(comment_model)
    sa.session.commit()
