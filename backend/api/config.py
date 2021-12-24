import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("SECRET_KEY", "very-simple-jwt-key")

class DevelopmentConfig(BaseConfig):
    pass

class ProductionConfig(BaseConfig):
    pass

config_dict = {"development": "DevelopmentConfig", "production":"ProductionConfig"}