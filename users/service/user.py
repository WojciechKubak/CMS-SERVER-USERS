from users.model.user import UserModel
from users.security.configuration import bcrypt
from dataclasses import dataclass
from typing import Any, ClassVar


@dataclass
class UserService:
    USER_NOT_FOUND_ERROR_MSG: ClassVar[str] = 'User not found'

    def add_user(self, data: dict[str, Any]) -> UserModel:
        if UserModel.find_by_username(data['username']) or UserModel.find_by_email(data['email']):
            raise ValueError('User already exists')
        hashed_password = bcrypt.generate_password_hash(data.pop('password'))
        user = UserModel(**data, password=hashed_password)
        user.add()
        return user

    def update_user(self, data: dict[str, Any]) -> UserModel:
        if not (user := UserModel.find_by_username(data['username'])):
            raise ValueError(self.USER_NOT_FOUND_ERROR_MSG)
        hashed_password = bcrypt.generate_password_hash(data.pop('password'))
        user.update(data | {'password': hashed_password})
        return user

    def delete_user(self, username: str) -> int:
        if not (user := UserModel.find_by_username(username)):
            raise ValueError(self.USER_NOT_FOUND_ERROR_MSG)
        user.delete()
        return user.id

    def activate_user(self, username: str) -> UserModel:
        if not (user := UserModel.find_by_username(username)):
            raise ValueError(self.USER_NOT_FOUND_ERROR_MSG)
        if user.is_active:
            raise ValueError('User is already active')
        user.update({'is_active': True})
        return user

    def check_login_credentials(self, username: str, password: str) -> UserModel:
        if not (user := UserModel.find_by_username(username)):
            raise ValueError(self.USER_NOT_FOUND_ERROR_MSG)
        if not user.check_password(password):
            raise ValueError('Incorrect password provided')
        if not user.is_active:
            raise ValueError('User is not activated')
        return user

    def get_user_by_name(self, username: str) -> UserModel:
        if not (user := UserModel.find_by_username(username)):
            raise ValueError(self.USER_NOT_FOUND_ERROR_MSG)
        return user

    def register_user(self, data: dict[str, Any]) -> UserModel:
        if UserModel.find_by_username(data['username']) or UserModel.find_by_email(data['email']):
            raise ValueError('User already exists')
        hashed_password = bcrypt.generate_password_hash(data.pop('password'))
        user = UserModel(**data, password=hashed_password)
        user.add()
        return user
