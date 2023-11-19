from users.email.configuration import MailConfig
from users.db.model import UserModel
from dataclasses import dataclass
from typing import Any


@dataclass
class UserService:

    def add_user(self, data: dict[str, Any]) -> UserModel:
        if UserModel.find_by_username(data.get('username')):
            raise ValueError('Username already in use')
        if UserModel.find_by_email(data.get('email')):
            raise ValueError('Email already in use')
        user = UserModel.from_json(data)
        user.add()
        return user

    def update_user(self, data: dict[str, Any]) -> UserModel:
        result = UserModel.find_by_username(data.get('username'))
        if not result:
            raise ValueError('User not found')
        user = UserModel.from_json(data)
        user.update()
        return user

    def delete_user(self, id_: str) -> int:
        result = UserModel.find_by_id(id_)
        if not result:
            raise ValueError('User not found')
        result.delete()
        return result.id

    def get_user_by_name(self, username: str) -> UserModel:
        result = UserModel.find_by_username(username)
        if not result:
            raise ValueError('User not found')
        return result

    def get_user_by_email(self, email: str) -> UserModel:
        result = UserModel.find_by_email(email)
        if not result:
            raise ValueError('User not found')
        return result

    def get_user_by_id(self, id_: int) -> UserModel:
        result = UserModel.find_by_id(id_)
        if not result:
            raise ValueError('User not found')
        return result

    def get_all_users(self) -> list[UserModel]:
        return UserModel.query.all()

    def activate_user(self, id_: int) -> UserModel:
        result = UserModel.find_by_id(id_)
        if not result:
            raise ValueError('User not found')
        if result.is_active:
            raise ValueError('User was already activated')
        result.set_active()
        return result

    def check_login_credentials(self, username: str, password: str) -> UserModel:
        result = UserModel.find_by_username(username)
        if not result:
            raise ValueError('User not found')
        if not result.check_password(password):
            raise ValueError('Incorrect password')
        if not result.is_active:
            raise ValueError('User is not activated')
        return result

    def register_user(self, data: dict[str, Any]) -> UserModel:
        if UserModel.find_by_username(data.get('username')):
            raise ValueError('Username already in use')
        if UserModel.find_by_email(data.get('email')):
            raise ValueError('Email already in use')
        user = UserModel.from_json(data)
        user.add()
        MailConfig.send_activation_mail(user.id, user.email)
        return user
