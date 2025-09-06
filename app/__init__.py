from flask import Flask
from flask_migrate import Migrate
from app.config import config
from app.db.models import db

def create_app(config_name='development'):
    """Фабрика приложения - создает и настраивает Flask приложение"""
    app = Flask(__name__)
    
    # Загружаем конфигурацию
    app.config.from_object(config[config_name])
    
    # Инициализируем расширения
    db.init_app(app)
    migrate = Migrate(app, db, directory='app/db/migrations')
    
    # Регистрируем Blueprint
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Импортируем модели для регистрации
    from app.db import models
    
    return app

# Создаем приложение для импорта
app = create_app('development')