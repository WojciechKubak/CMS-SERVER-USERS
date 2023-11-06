import os


class Config:
    TESTING = False
    DATABASE_URI = 'mysql://user:user1234@mysql:3307/db_1'


class ProductionConfig(Config):
    TESTING = False
    DATABASE_URI = os.environ.get('DATABASE_URI')


class DevelopmentConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_URI = 'mysql://user:user1234@localhost:3308/db_test'


def call_configuration() -> type[Config]:
    match os.environ.get('APP_CONFIG', '').lower():
        case 'production':
            return ProductionConfig
        case 'development':
            return DevelopmentConfig
        case _:
            return Config
