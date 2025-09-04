import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Конфигурация для разработки"""
    DEBUG = True
    FLASK_ENV = 'development'

# Выбор конфигурации
config = {
    'development': DevelopmentConfig
}
