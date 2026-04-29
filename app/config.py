import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY=os.getenv("SECRET_KEY","dev-secret-change-this")
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY","dev-jwt-secret-change-this")
    SQLALCHEMY_TRACK_MODIFICATIONS=False

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