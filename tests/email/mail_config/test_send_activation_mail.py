from users.email.configuration import MailConfig
from flask import Flask
from typing import Any


def test_send_activation_mail(app: Flask, user_model_data: dict[str, Any]) -> None:
    with MailConfig.mail.record_messages() as outbox:
        email = user_model_data['email']

        MailConfig.send_activation_mail(user_model_data['id'], email)

        assert "Activate your account" == outbox[0].subject
        assert [email] == outbox[0].recipients
        assert 'Click to activate your account' in outbox[0].html
