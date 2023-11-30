from users.model.user import UserModel
from flask.testing import Client


def test_user_list_resource_get(client: Client) -> None:
    response = client.get('/users')
    assert 200 == response.status_code
    assert len(UserModel.query.all()) == len(response.json)
