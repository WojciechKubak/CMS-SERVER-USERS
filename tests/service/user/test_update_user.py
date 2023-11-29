from users.service.user import UserService
from typing import Any
import pytest


class TestUserServiceUpdateUser:
    def test_when_user_does_not_exist(self, user_service: UserService, user_dto: dict[str, Any]) -> None:
        with pytest.raises(ValueError) as e:
            user_service.update_user(user_dto | {'username': f"111{user_dto['username']}"})
        assert 'User not found' == str(e.value)

    def test_when_updated_succesfully(self, user_service: UserService, user_dto: dict[str, Any]) -> None:
        new_email = f"New{user_dto['email']}"
        result = user_service.update_user(user_dto | {'email': new_email})
        assert new_email == result.email
