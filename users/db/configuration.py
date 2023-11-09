from users.config import get_configuration
from users.db.repository import UserRepository
from sqlalchemy import create_engine

engine = create_engine(get_configuration().DATABASE_URI)

user_repository = UserRepository(engine)
