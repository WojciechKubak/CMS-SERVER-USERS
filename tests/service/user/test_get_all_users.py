from users.service.user import UserService
from users.model.user import UserModel


class TestUserServiceGetAllUsers:

    def test_when_no_users(self, user_service: UserService) -> None:
        UserModel.query.delete()
        assert not user_service.get_all_users()

    def test_when_users_are_present(self, user_service: UserService) -> None:
        result = user_service.get_all_users()
        expected = UserModel.query.all()
        assert len(expected) == len(result)
