from users.db.configuration import sa
from users.model.user import UserModel
from flask import Flask
from typing import Any
import pytest


@pytest.fixture(scope='function', autouse=True)
def add_user(app: Flask, user_model_data: dict[str, Any]) -> None:
    sa.session.add(UserModel(**user_model_data))
    sa.session.commit()
