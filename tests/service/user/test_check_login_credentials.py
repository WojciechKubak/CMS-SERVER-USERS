from users.service.user import UserService
from users.model.user import UserModel
from unittest.mock import patch, PropertyMock
from typing import Any
import pytest


class TestUserServiceCheckLoginCredentials:

    def test_when_user_does_not_exist(self, user_service: UserService, user_dto: dict[str, Any]) -> None:
        with pytest.raises(ValueError) as e:
            user_service.check_login_credentials(f"111{user_dto['username']}", user_dto['password'])
        assert 'User not found' == str(e.value)

    def test_when_password_is_incorrect(self, user_service: UserService, user_dto: dict[str, Any]) -> None:
        with pytest.raises(ValueError) as e:
            user_service.check_login_credentials(user_dto['username'], f"111{user_dto['password']}")
        assert 'Incorrect password' == str(e.value)

    def test_when_user_is_inactive(self, user_service: UserService, user_dto: dict[str, Any]) -> None:
        with pytest.raises(ValueError) as e:
            user_service.check_login_credentials(user_dto['username'], user_dto['password'])
        assert 'User is not activated' == str(e.value)

    def test_when_credential_are_correct(self, user_service: UserService, user_dto: dict[str, Any]) -> None:
        with patch.object(UserModel, 'is_active', new_callable=PropertyMock) as attr_mock:
            attr_mock.return_value = True
            result = user_service.check_login_credentials(user_dto['username'], user_dto['password'])
        expected = UserModel.query.filter_by(username=user_dto['username']).first()
        assert expected.username == result.username
