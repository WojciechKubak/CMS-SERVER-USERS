from users.model.user import UserModel
from users.model.comment import CommentModel
from users.db.configuration import sa
from flask import Flask
from typing import Any, Callable
import pytest


@pytest.fixture(scope='session')
def user_model_with_id(user_model_data: dict[str, Any]) -> Callable[[int], UserModel]:
    def create_user(id_: int) -> UserModel:
        return UserModel(**user_model_data | {'id': id_})
    return create_user


@pytest.fixture
def user_model(user_model_with_id: Callable[[int], UserModel]) -> UserModel:
    return user_model_with_id(1)


@pytest.fixture(autouse=True)
def add_user(app: Flask, user_model: UserModel) -> None:
    sa.session.add(user_model)
    sa.session.commit()
