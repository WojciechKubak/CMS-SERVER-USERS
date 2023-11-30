from users.model.user import UserModel


def test_comment_model_to_json(comment_model: UserModel) -> None:
    result = comment_model.to_json()
    assert comment_model.__dict__.items() > result.items()
