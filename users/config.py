from dotenv import load_dotenv
import ast
import os

load_dotenv()


class Config(object):
    """Base configuration class with common settings for all environments."""
    TESTING = False

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql://user:user1234@mysql:3307/db_1'


class ProductionConfig(Config):
    """Production environment configuration."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DB_URI', '')


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql://user:user1234@localhost:3308/db_test'


app_config = {
        'production': ProductionConfig,
        'development': DevelopmentConfig,
        'testing': TestingConfig
    }.get(os.environ.get('APP_CONFIG', '').lower(), Config)

security_config = {
        'JWT_COOKIE_SECURE': ast.literal_eval(os.environ.get('JWT_COOKIE_SECURE')),
        'JWT_TOKEN_LOCATION': ast.literal_eval(os.environ.get('JWT_TOKEN_LOCATION')),
        'JWT_SECRET_KEY': os.environ.get('JWT_SECRET_KEY'),
        'JWT_ACCESS_TOKEN_EXPIRES': int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES')),
        'JWT_REFRESH_TOKEN_EXPIRES': int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES')),
        'JWT_COOKIE_CSRF_PROTECT': ast.literal_eval(os.environ.get('JWT_COOKIE_CSRF_PROTECT'))
    }

mail_config = {
        'MAIL_SERVER': os.environ.get('MAIL_SERVER'),
        'MAIL_PORT': int(os.environ.get('MAIL_PORT')),
        'MAIL_USE_SSL': ast.literal_eval(os.environ.get('MAIL_USE_SSL')),
        'MAIL_USE_TLS': ast.literal_eval(os.environ.get('MAIL_USE_TLS')),
        'MAIL_USERNAME': os.environ.get('MAIL_USERNAME'),
        'MAIL_PASSWORD': os.environ.get('MAIL_PASSWORD')
    }
