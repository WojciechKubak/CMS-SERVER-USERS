from users.service.user import UserService
import pytest


@pytest.fixture(scope='session')
def user_service() -> UserService:
    return UserService()
