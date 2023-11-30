from users.model.user import UserModel


def test_set_active(user_model: UserModel) -> None:
    user_model.set_active()
    assert UserModel.query.filter_by(id=user_model.id).first().is_active
