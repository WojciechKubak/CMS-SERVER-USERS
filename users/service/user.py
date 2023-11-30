from users.email.configuration import MailConfig
from users.model.user import UserModel
from dataclasses import dataclass
from typing import Any


@dataclass
class UserService:
    """Service class for handling operations related to users."""

    def add_user(self, data: dict[str, Any]) -> UserModel:
        """
        Add a new user based on the provided data.

        Args:
            data (dict[str, Any]): Data for creating the new user.

        Returns:
            UserModel: The created user.
        """
        if UserModel.find_by_username(data.get('username')):
            raise ValueError('Username already in use')
        if UserModel.find_by_email(data.get('email')):
            raise ValueError('Email already in use')
        user = UserModel.from_json(data)
        user.add()
        return user

    def update_user(self, data: dict[str, Any]) -> UserModel:
        """
        Update a user based on the provided data.

        Args:
            data (dict[str, Any]): Data for updating the user.

        Returns:
            UserModel: The updated user.
        """
        result = UserModel.find_by_id(data.pop('id'))
        if not result:
            raise ValueError('User not found')
        filtered_data = {key: val for key, val in data.items() if val}
        user = UserModel.from_json(result.to_json() | filtered_data)
        user.update()
        return user

    def delete_user(self, id_: str) -> int:
        """
        Delete a user by their ID.

        Args:
            id_ (str): The ID of the user to delete.

        Returns:
            int: The ID of the deleted user.
        """
        result = UserModel.find_by_id(id_)
        if not result:
            raise ValueError('User not found')
        result.delete()
        return result.id

    def get_user_by_name(self, username: str) -> UserModel:
        """
        Get a user by their username.

        Args:
            username (str): The username of the user.

        Returns:
            UserModel: The retrieved user.
        """
        result = UserModel.find_by_username(username)
        if not result:
            raise ValueError('User not found')
        return result

    def get_user_by_email(self, email: str) -> UserModel:
        """
        Get a user by their email.

        Args:
            email (str): The email of the user.

        Returns:
            UserModel: The retrieved user.
        """
        result = UserModel.find_by_email(email)
        if not result:
            raise ValueError('User not found')
        return result

    def get_user_by_id(self, id_: int) -> UserModel:
        """
        Get a user by their ID.

        Args:
            id_ (int): The ID of the user.

        Returns:
            UserModel: The retrieved user.
        """
        result = UserModel.find_by_id(id_)
        if not result:
            raise ValueError('User not found')
        return result

    def get_all_users(self) -> list[UserModel]:
        """
        Get a list of all users.

        Returns:
            list[UserModel]: List of all users.
        """
        return UserModel.query.all()

    def activate_user(self, id_: int) -> UserModel:
        """
        Activate a user by their ID.

        Args:
            id_ (int): The ID of the user to activate.

        Returns:
            UserModel: The activated user.
        """
        result = UserModel.find_by_id(id_)
        if not result:
            raise ValueError('User not found')
        if result.is_active:
            raise ValueError('User was already activated')
        result.set_active()
        return result

    def check_login_credentials(self, username: str, password: str) -> UserModel:
        """
        Check login credentials and return the user.

        Args:
            username (str): The username of the user.
            password (str): The password for login.

        Returns:
            UserModel: The authenticated user.
        """
        result = UserModel.find_by_username(username)
        if not result:
            raise ValueError('User not found')
        if not result.check_password(password):
            raise ValueError('Incorrect password')
        if not result.is_active:
            raise ValueError('User is not activated')
        return result

    def register_user(self, data: dict[str, Any]) -> UserModel:
        """
        Register a new user based on the provided data and send an activation email.

        Args:
            data (dict[str, Any]): Data for creating the new user.

        Returns:
            UserModel: The created user.
        """
        if UserModel.find_by_username(data.get('username')):
            raise ValueError('Username already in use')
        if UserModel.find_by_email(data.get('email')):
            raise ValueError('Email already in use')
        user = UserModel.from_json(data)
        user.add()
        MailConfig.send_activation_mail(user.id, user.email)
        return user
