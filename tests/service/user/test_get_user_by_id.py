from users.service.user import UserService
from users.model.user import UserModel
from typing import Any
import pytest


class TestUserServiceGetUserById:

    @pytest.fixture(scope='session')
    def user_id(self, user_model_data: dict[str, Any]) -> int:
        return user_model_data['id']

    def test_when_user_not_found(self, user_service: UserService) -> None:
        with pytest.raises(ValueError) as e:
            user_service.get_user_by_id(1111)
        assert 'User not found' == str(e.value)

    def test_when_user_found_sucessfully(self, user_service: UserService, user_id: int) -> None:
        result = user_service.get_user_by_id(user_id)
        expected = UserModel.query.filter_by(id=user_id).first()
        assert expected.username == result.username
