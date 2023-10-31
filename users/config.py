from dataclasses import dataclass
from typing import Type
import os


@dataclass
class BaseConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://user:user1234@mysql:3307/db_1'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


@dataclass
class ProductionConfig(BaseConfig):
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')


@dataclass
class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


@dataclass
class TestingConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql://user:user1234@localhost:3308/db_test'


def get_config() -> Type[BaseConfig]:
    return {
        'production': ProductionConfig,
        'development': DevelopmentConfig,
        'testing': TestingConfig
    }.get(os.environ.get('APP_CONFIG'), BaseConfig)
