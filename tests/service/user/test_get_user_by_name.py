from users.service.user import UserService
from users.model.user import UserModel
from typing import Any
import pytest


class TestUserServiceGetUserByName:

    @pytest.fixture(scope='session')
    def user_username(self, user_dto: dict[str, Any]) -> str:
        return user_dto['username']

    def test_when_user_not_found(self, user_service: UserService, user_username: str) -> None:
        with pytest.raises(ValueError) as e:
            user_service.get_user_by_name(f"111{user_username}")
        assert 'User not found' == str(e.value)

    def test_when_user_found_sucessfully(self, user_service: UserService, user_username: str) -> None:
        result = user_service.get_user_by_name(user_username)
        expected = UserModel.query.filter_by(username=user_username).first()
        assert expected.username == result.username
