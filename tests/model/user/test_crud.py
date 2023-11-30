from users.model.user import UserModel
from users.db.configuration import sa
from typing import Any, Callable


class TestUserModelCrud:

    def test_add(self, user_model_with_id: Callable[[int], UserModel]) -> None:
        new_id = 9999
        user_with_new_id = user_model_with_id(new_id)
        user_with_new_id.add()
        assert sa.session.query(UserModel).filter_by(id=new_id).first()

    def test_update(self, user_model_data: dict[str, Any]) -> None:
        new_email = 'new@example.com'
        user_with_existing_id = UserModel(**user_model_data | {'email': new_email})
        user_with_existing_id.update()
        expected = sa.session.query(UserModel).filter_by(id=user_model_data['id']).first().email
        assert new_email == expected

    def test_delete(self, user_model: UserModel) -> None:
        id_to_delete = user_model.id
        user_model.delete()
        assert not sa.session.query(UserModel).filter_by(id=id_to_delete).first()

    def test_find_by_id(self, user_model: UserModel) -> None:
        assert user_model == UserModel.find_by_id(user_model.id)

    def test_find_by_username(self, user_model: UserModel) -> None:
        assert user_model == UserModel.find_by_username(user_model.username)

    def test_find_by_email(self, user_model: UserModel) -> None:
        assert user_model == UserModel.find_by_email(user_model.email)
