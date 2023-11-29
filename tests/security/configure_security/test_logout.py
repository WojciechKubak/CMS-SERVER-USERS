from flask.testing import Client


def test_logout(client: Client, access_token: str) -> None:
    client.set_cookie('access_token_cookie', access_token)
    response_logout = client.post('/logout')

    assert response_logout.status_code == 200
    assert b'Logout successful' in response_logout.data
    assert not client.get_cookie('access_token_cookie')
