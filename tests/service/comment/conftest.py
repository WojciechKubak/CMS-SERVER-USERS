from users.service.comment import CommentService
from users.db.configuration import sa
from users.model.comment import CommentModel
from flask import Flask
from typing import Any
import pytest


@pytest.fixture(scope='session')
def comment_service() -> CommentService:
    return CommentService()


@pytest.fixture(scope='function', autouse=True)
def add_comment(app: Flask, comment_model_data: dict[str, Any]) -> None:
    sa.session.add(CommentModel(**comment_model_data))
    sa.session.commit()
