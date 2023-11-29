from users.service.user import UserService
from users.model.user import UserModel
from unittest.mock import patch, PropertyMock
from typing import Any
import pytest


class TestUserServiceActivateUser:

    @pytest.fixture(scope='session')
    def user_id(self, user_model_data: dict[str, Any]) -> int:
        return user_model_data['id']

    def test_when_user_does_not_exist(self, app, user_service: UserService) -> None:
        with pytest.raises(ValueError) as e:
            user_service.activate_user(1111)
        assert 'User not found' == str(e.value)

    def test_when_user_is_already_active(self, user_service: UserService, user_id: int) -> None:
        with patch.object(UserModel, 'is_active', new_callable=PropertyMock) as attr_mock:
            attr_mock.return_value = True

            with pytest.raises(ValueError) as e:
                user_service.activate_user(user_id)

            assert 'User was already activated' == str(e.value)

    def test_when_user_activated_succesfully(self, user_service: UserService, user_id: int) -> None:
        result = user_service.activate_user(user_id)
        assert UserModel.query.filter_by(id=result.id).first().is_active
