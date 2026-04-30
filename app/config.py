import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY=os.getenv("SECRET_KEY","dev-secret-change-this")
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY","dev-jwt-secret-change-this")
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI="sqlite:///ecommerce.db"

class ProductionConfig(Config):
    DEBUG=False
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL","")

config_map={
    "development":DevelopmentConfig,
    "production":ProductionConfig,
}
def get_config():
    env=os.getenv("FLASK_ENV","development")
    return config_map.get(env,DevelopmentConfig)