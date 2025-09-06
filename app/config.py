import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Connection pooling для лучшей производительности
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 20,
        'pool_timeout': 30
    }
    
    # Настройки для production
    SQLALCHEMY_RECORD_QUERIES = False

class DevelopmentConfig(Config):
    """Конфигурация для разработки"""
    DEBUG = True
    FLASK_ENV = 'development'
    
    # Более мягкие настройки для разработки
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 10,
        'pool_timeout': 30,
        'echo': False  # Установите True для отладки SQL запросов
    }

class ProductionConfig(Config):
    """Конфигурация для production"""
    DEBUG = False
    FLASK_ENV = 'production'
    
    # Более агрессивные настройки для production
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 30,
        'pool_timeout': 30
    }

# Выбор конфигурации
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
