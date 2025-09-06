from flask import Blueprint, jsonify
from app.db.models import db
from app.logger import log_info
from app.health import health_checker

# Создаем Blueprint для маршрутов
main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
    log_info("Home page accessed")
    return "Chess Puzzles Bot API - Hello from Docker!"

@main_bp.route("/health")
def health():
    """Основной health check endpoint"""
    log_info("Health check requested")
    health_status = health_checker.get_comprehensive_health()
    
    # Возвращаем соответствующий HTTP статус код
    status_code = 200 if health_status["status"] == "healthy" else 503
    return jsonify(health_status), status_code

@main_bp.route("/health/app")
def health_app():
    """Проверка состояния приложения"""
    log_info("App health check requested")
    return jsonify(health_checker.get_app_health())

@main_bp.route("/health/database")
def health_database():
    """Проверка состояния базы данных"""
    log_info("Database health check requested")
    db_health = health_checker.get_database_health()
    status_code = 200 if db_health["status"] == "healthy" else 503
    return jsonify(db_health), status_code

@main_bp.route("/health/rabbitmq")
def health_rabbitmq():
    """Проверка состояния RabbitMQ"""
    log_info("RabbitMQ health check requested")
    rabbitmq_health = health_checker.get_rabbitmq_health()
    status_code = 200 if rabbitmq_health["status"] == "healthy" else 503
    return jsonify(rabbitmq_health), status_code
