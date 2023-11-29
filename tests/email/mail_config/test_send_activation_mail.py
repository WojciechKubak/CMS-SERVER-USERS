from users.email.configuration import MailConfig
from flask import Flask
from typing import Any


def test_send_activation_mail(app: Flask, user_model_data: dict[str, Any]) -> None:
    with MailConfig.mail.record_messages() as outbox:
        id_, email = 1, 'user@example.com'

        MailConfig.send_activation_mail(user_model_data['id'], user_model_data['email'])

        assert 1 == len(outbox)
        assert "Activate your account" == outbox[0].subject
        assert [email] == outbox[0].recipients
        assert 'Click to activate your account' in outbox[0].html
