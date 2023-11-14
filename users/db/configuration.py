from users.config import app_config
from users.db.repository import UserRepository
from sqlalchemy import create_engine

engine = create_engine(app_config.DATABASE_URI)

user_repository = UserRepository(engine)
