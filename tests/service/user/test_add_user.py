from users.service.user import UserService
from users.model.user import UserModel
from typing import Any
import pytest


class TestUserServiceAddUser:

    def test_when_username_already_exists(self, user_service: UserService, user_dto: dict[str, Any]) -> None:
        with pytest.raises(ValueError) as e:
            user_service.add_user(user_dto)
        assert 'Username already in use' == str(e.value)

    def test_when_email_already_exists(self, user_service: UserService, user_dto: dict[str, Any]) -> None:
        with pytest.raises(ValueError) as e:
            user_service.add_user(user_dto | {'username': f"New{user_dto['username']}"})
        assert 'Email already in use' == str(e.value)

    def test_when_user_added_successfully(self, user_service: UserService, user_dto: dict[str, Any]) -> None:
        new_user_data = {k: v + 'new' for k, v in user_dto.items()}
        result = user_service.add_user(new_user_data)
        assert UserModel.query.filter_by(username=result.username).first()
