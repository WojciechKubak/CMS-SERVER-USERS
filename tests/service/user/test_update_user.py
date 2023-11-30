from users.service.user import UserService
from typing import Any
import pytest


class TestUserServiceUpdateUser:
    def test_when_user_does_not_exist(self, user_service: UserService, user_model_data: dict[str, Any]) -> None:
        with pytest.raises(ValueError) as e:
            user_service.update_user(user_model_data | {'id': 1111})
        assert 'User not found' == str(e.value)

    def test_when_updated_succesfully(self, user_service: UserService, user_model_data: dict[str, Any]) -> None:
        new_email = 'new@example.com'
        result = user_service.update_user(user_model_data | {'email': new_email})
        assert new_email == result.email
