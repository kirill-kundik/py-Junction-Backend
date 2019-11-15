import os
import pathlib

from dotenv import load_dotenv

PROJECT_ROOT = pathlib.Path(__file__).parent
load_dotenv(dotenv_path=PROJECT_ROOT.parent / '.env')


class Config:
    FLASK_APP = "app"
    PORT = os.getenv("APP_PORT")
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    DATABASE_URI = f'postgres+psycopg2://' \
                   f'{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@' \
                   f'{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
