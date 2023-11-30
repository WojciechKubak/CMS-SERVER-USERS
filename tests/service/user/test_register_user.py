from users.service.user import UserService
from users.model.user import UserModel
from typing import Any
import pytest


class TestUserServiceRegisterUser:
    username = 'newUsername'
    email = 'new@example.com'

    def test_when_username_already_exists(self, user_service: UserService, user_dto: dict[str, Any]) -> None:
        with pytest.raises(ValueError) as e:
            user_service.register_user(user_dto)
        assert 'Username already in use' == str(e.value)

    def test_when_email_already_exists(self, user_service: UserService, user_dto: dict[str, Any]) -> None:
        with pytest.raises(ValueError) as e:
            user_service.register_user(user_dto | {'username': self.username})
        assert 'Email already in use' == str(e.value)

    def test_when_registered_succesfully(self, user_service: UserService, user_dto: dict[str, Any]) -> None:
        result = user_service.register_user(user_dto | {'username': self.username, 'email': self.email})
        expected = UserModel.query.filter_by(username=self.username).first()
        assert expected.username == result.username
