"""
Упрощенный модуль для проверки состояния компонентов системы
"""
import os
import time
from datetime import datetime, timezone
from typing import Dict, Any
import pika
from sqlalchemy import text
from app.db.models import db
from app.logger import log_error


class HealthChecker:
    """Упрощенный класс для проверки состояния компонентов системы"""
    
    def __init__(self):
        self.start_time = datetime.now(timezone.utc)
    
    def get_app_health(self) -> Dict[str, Any]:
        """Проверка состояния приложения"""
        start_time = time.time()
        try:
            uptime_delta = datetime.now(timezone.utc) - self.start_time
            uptime_seconds = uptime_delta.total_seconds()
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            return {
                "status": "healthy",
                "uptime_seconds": uptime_seconds,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "version": "1.0.0",
                "response_time_ms": round(response_time, 2)
            }
        except Exception as e:
            log_error(f"App health check failed: {e}")
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "response_time_ms": round(response_time, 2)
            }
    
    def get_database_health(self) -> Dict[str, Any]:
        """Проверка состояния базы данных"""
        start_time = time.time()
        try:
            with db.engine.connect() as conn:
                # Простой запрос для проверки подключения
                result = conn.execute(text("SELECT 1")).fetchone()
                
                if result[0] != 1:
                    raise Exception("Database connection test failed")
                
                # Проверяем только количество головоломок
                puzzle_count = conn.execute(text("SELECT COUNT(*) FROM puzzle")).fetchone()[0]
                
                end_time = time.time()
                response_time = (end_time - start_time) * 1000
                return {
                    "status": "healthy",
                    "connection": "ok",
                    "puzzle_count": puzzle_count,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "response_time_ms": round(response_time, 2)
                }
                
        except Exception as e:
            log_error(f"Database health check failed: {e}")
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            return {
                "status": "unhealthy",
                "connection": "failed",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "response_time_ms": round(response_time, 2)
            }
    
    def get_rabbitmq_health(self) -> Dict[str, Any]:
        """Проверка состояния RabbitMQ"""
        start_time = time.time()
        try:
            # Параметры подключения к RabbitMQ
            rabbitmq_host = os.getenv('RABBITMQ_HOST')
            rabbitmq_port = int(os.getenv('RABBITMQ_PORT'))
            rabbitmq_user = os.getenv('RABBITMQ_DEFAULT_USER')
            rabbitmq_password = os.getenv('RABBITMQ_DEFAULT_PASS')
            
            # Подключаемся к RabbitMQ
            credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
            parameters = pika.ConnectionParameters(
                host=rabbitmq_host,
                port=rabbitmq_port,
                credentials=credentials,
                heartbeat=30,
                blocked_connection_timeout=10
            )
            
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            
            # Проверяем доступность сервера
            channel.queue_declare(queue='health_check', durable=False, auto_delete=True)
            channel.queue_delete(queue='health_check')
            
            connection.close()
            
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            return {
                "status": "healthy",
                "connection": "ok",
                "host": rabbitmq_host,
                "port": rabbitmq_port,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "response_time_ms": round(response_time, 2)
            }
            
        except Exception as e:
            log_error(f"RabbitMQ health check failed: {e}")
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            return {
                "status": "unhealthy",
                "connection": "failed",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "host": rabbitmq_host if 'rabbitmq_host' in locals() else "unknown",
                "port": rabbitmq_port if 'rabbitmq_port' in locals() else "unknown",
                "response_time_ms": round(response_time, 2)
            }
    
    def get_comprehensive_health(self) -> Dict[str, Any]:
        """Комплексная проверка состояния всех компонентов"""
        start_time = time.time()
        
        # Получаем статус всех компонентов
        app_health = self.get_app_health()
        db_health = self.get_database_health()
        rabbitmq_health = self.get_rabbitmq_health()
        
        # Определяем общий статус
        all_healthy = all([
            app_health.get("status") == "healthy",
            db_health.get("status") == "healthy",
            rabbitmq_health.get("status") == "healthy"
        ])
        
        overall_status = "healthy" if all_healthy else "unhealthy"
        response_time = time.time() - start_time
        
        return {
            "status": overall_status,
            "response_time_ms": round(response_time * 1000, 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "components": {
                "application": app_health,
                "database": db_health,
                "rabbitmq": rabbitmq_health
            },
            "summary": {
                "total_components": 3,
                "healthy_components": sum([
                    1 for comp in [app_health, db_health, rabbitmq_health]
                    if comp.get("status") == "healthy"
                ]),
            }
        }


# Глобальный экземпляр health checker
health_checker = HealthChecker()
