from flask import Flask
from app.config import config
from app.database import db, init_db

def create_app(config_name='development'):
    """Фабрика приложения - создает и настраивает Flask приложение"""
    app = Flask(__name__)
    
    # Загружаем конфигурацию
    app.config.from_object(config[config_name])
    
    # Инициализируем расширения
    db.init_app(app)
    
    # Регистрируем Blueprint
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Импортируем модели для регистрации
    from app import models
    
    # Инициализируем базу данных
    init_db(app)
    
    return app

# Создаем приложение для импорта
app = create_app('development')