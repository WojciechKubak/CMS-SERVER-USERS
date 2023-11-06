from users.db.entity import UserEntity
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Engine
from dataclasses import dataclass, field
from typing import Callable, Any, Self
from functools import wraps


def transactional(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args: tuple[Any], **kwargs: dict[str, Any]):
        try:
            result = method(self, *args, **kwargs)
            self.session.commit()
            return result
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    return wrapper


@dataclass
class CrudRepository:
    _engine: Engine
    _entity: type

    def __post_init__(self):
        session_maker = sessionmaker(bind=self._engine, expire_on_commit=False)
        self.session = session_maker(expire_on_commit=False)

    @transactional
    def add(self, item: Any) -> None:
        self.session.add(item)

    @transactional
    def update(self, item: Any) -> None:
        self.session.merge(item)

    @transactional
    def delete(self, id_: int) -> None:
        item = self.session.query(self._entity).filter_by(id=id_).first()
        self.session.delete(item)

    @transactional
    def find_by_id(self, id_: int) -> type | None:
        return self.session.query(self._entity).filter_by(id=id_).first()

    @transactional
    def get_all(self) -> list[type]:
        return self.session.query(self._entity).all()


@dataclass
class UserRepository(CrudRepository):
    _engine: Engine
    _entity: type = field(default=UserEntity, init=False)

    @transactional
    def find_by_username(self, username: str) -> Self:
        return self.session.query(self._entity).filter_by(username=username).first()

    @transactional
    def find_by_email(self, email: str) -> Self:
        return self.session.query(self._entity).filter_by(email=email).first()
