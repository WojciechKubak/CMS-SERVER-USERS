from users.model.user import UserModel
from typing import Any


def test_user_model_from_json(user_dto: dict[str, Any]) -> None:
    user = UserModel.from_json(user_dto)

    user_dto_copy = user_dto.copy()
    dto_password = user_dto_copy.pop('password')

    assert user_dto_copy.items() < user.__dict__.items()
    assert user.check_password(dto_password)
