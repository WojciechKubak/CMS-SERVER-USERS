import os


class Config(object):
    DEBUG = False
    TESTING = False

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DATABASE_URI = 'mysql://user:user1234@mysql:3307/db_1'

    SESSION_COOKIE_SECURE = True


class ProductionConfig(Config):
    DATABASE_URI = os.environ.get('PRODUCTION_DB_URI', '')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_URI = 'mysql://user:user1234@localhost:3308/db_test'

    SESSION_COOKIE_SECURE = False


def get_configuration() -> type[Config]:
    match os.environ.get('APP_CONFIG', '').lower():
        case 'production':
            return ProductionConfig
        case 'development':
            return DevelopmentConfig
        case _:
            return Config
