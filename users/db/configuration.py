from users.config import call_configuration
from users.db.repository import UserRepository
from sqlalchemy import create_engine

engine = create_engine(call_configuration().DATABASE_URI)

user_repository = UserRepository(engine)
