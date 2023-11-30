from users.model.user import UserModel


def test_user_model_to_json(user_model: UserModel) -> None:
    result = user_model.to_json()
    assert user_model.__dict__.items() > result.items()
