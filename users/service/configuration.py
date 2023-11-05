from users.db.configuration import user_repository
from users.service.user import UserService

user_service = UserService(user_repository)
