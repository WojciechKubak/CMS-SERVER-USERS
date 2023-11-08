from users.db.configuration import UserRepository
from users.email.configuration import MailConfig
from users.security.configuration import bcrypt
from users.db.entity import UserEntity
from dataclasses import dataclass
from typing import Any


@dataclass
class UserService:
    user_repository: UserRepository

    def add_user(self, data: dict[str, Any]) -> UserEntity:
        if self.user_repository.find_by_username(data.get('username')):
            raise ValueError('Username already in use')
        if self.user_repository.find_by_email(data.get('email')):
            raise ValueError('Email already in use')

        hashed_password = bcrypt.generate_password_hash(data.pop('password'))
        new_user = UserEntity(**data, password=hashed_password)
        self.user_repository.add(new_user)

        return new_user

    def update_user(self, data: dict[str, Any]) -> UserEntity:
        result = self.user_repository.find_by_username(data.get('username'))
        if not result:
            raise ValueError('User not found')

        hashed_password = bcrypt.generate_password_hash(data.pop('password'))
        updated_user = UserEntity(**data, password=hashed_password)
        self.user_repository.update(updated_user)

        return updated_user

    def delete_user(self, id_: str) -> int:
        result = self.user_repository.find_by_id(id_)
        if not result:
            raise ValueError('User not found')
        self.user_repository.delete(result.id)
        return result.id

    def get_user_by_name(self, username: str) -> UserEntity:
        result = self.user_repository.find_by_username(username)
        if not result:
            raise ValueError('User not found')
        return result

    def get_user_by_email(self, email: str) -> UserEntity:
        result = self.user_repository.find_by_email(email)
        if not result:
            raise ValueError('User not found')
        return result

    def get_user_by_id(self, id_: int) -> UserEntity:
        result = self.user_repository.find_by_id(id_)
        if not result:
            raise ValueError('User not found')
        return result

    def get_all_users(self) -> list[UserEntity]:
        return self.user_repository.get_all()

    def activate_user(self, id_: int) -> UserEntity:
        result = self.user_repository.find_by_id(id_)
        if not result:
            raise ValueError('User not found')
        if result.is_active:
            raise ValueError('User was already activated')

        result.is_active = True
        self.user_repository.update(result)

        return result

    def check_login_credentials(self, username: str, password: str) -> UserEntity:
        result = self.user_repository.find_by_username(username)
        if not result:
            raise ValueError('User not found')
        if not bcrypt.check_password_hash(result.password, password):
            raise ValueError('Incorrect password')
        if not result.is_active:
            raise ValueError('User is not activated')
        return result

    def register_user(self, data: dict[str, Any]) -> UserEntity:
        if self.user_repository.find_by_username(data.get('username')):
            raise ValueError('Username already in use')
        if self.user_repository.find_by_email(data.get('email')):
            raise ValueError('Email already in use')

        hashed_password = bcrypt.generate_password_hash(data.pop('password'))
        user = UserEntity(**data, password=hashed_password)
        self.user_repository.add(user)
        MailConfig.send_activation_mail(user.id, user.email)

        return user
