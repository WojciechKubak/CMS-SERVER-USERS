from users.service.user import UserService
from users.model.user import UserModel
from typing import Any
import pytest


class TestUserServiceGetUserByEmail:

    @pytest.fixture(scope='session')
    def user_email(self, user_dto: dict[str, Any]) -> str:
        return user_dto['email']

    def test_when_user_not_found(self, user_service: UserService, user_email: str) -> None:
        with pytest.raises(ValueError) as e:
            user_service.get_user_by_email(f"111{user_email}")
        assert 'User not found' == str(e.value)

    def test_when_user_found_sucessfully(self, user_service: UserService, user_email: str) -> None:
        result = user_service.get_user_by_email(user_email)
        expected = UserModel.query.filter_by(email=user_email).first()
        assert expected.username == result.username
