from users.service.user import UserService
from users.model.user import UserModel
from typing import Any
import pytest


class TestUserServiceDeleteUser:

    def test_when_user_does_not_exist(self, user_service: UserService, user_model_data: dict[str, Any]) -> None:
        with pytest.raises(ValueError) as e:
            user_service.check_login_credentials(f"111{user_model_data['username']}", user_model_data['password'])
        assert 'User not found' == str(e.value)

    def test_when_deleted_successfully(self, user_service: UserService, user_model_data: dict[str, Any]) -> None:
        result = user_service.delete_user(user_model_data['id'])
        assert not UserModel.query.filter_by(id=result).first()
