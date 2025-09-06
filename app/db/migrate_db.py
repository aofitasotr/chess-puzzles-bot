#!/usr/bin/env python3
"""
Скрипт для управления миграциями базы данных
"""

import os
import sys
import time
from dotenv import load_dotenv
from flask_migrate import upgrade, init, migrate
import psycopg2
from psycopg2 import OperationalError

# Загружаем переменные окружения
load_dotenv()

# Импортируем логгер
from app.logger import log_info, log_error

def wait_for_postgres(max_retries=30, retry_delay=3):
    """Ждет готовности PostgreSQL"""
    log_info("Waiting for PostgreSQL to be ready...")
    
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=os.getenv('POSTGRES_HOST'),
                port=os.getenv('POSTGRES_PORT'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                dbname=os.getenv('POSTGRES_DB')
            )
            conn.close()
            log_info("PostgreSQL is ready!")
            return True
        except OperationalError:
            log_info(f"PostgreSQL is unavailable - attempt {attempt + 1}/{max_retries}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
    
    log_error("PostgreSQL is not ready after all attempts")
    return False

def run_migrations():
    """Выполняет миграции с автоматической инициализацией"""
    try:
        from app import create_app
        
        app = create_app()
        with app.app_context():
            log_info("Setting up database migrations...")
            
            # Инициализируем миграции (создаст папку и файлы если нужно)
            try:
                init()
                log_info("Migrations initialized")
            except:
                log_info("Migrations already exist")
            
            # Создаем начальную миграцию если нужно
            try:
                migrate(message="Initial migration")
                log_info("Initial migration created")
            except:
                log_info("Migration already exists")
            
            # Применяем все миграции
            log_info("Applying migrations...")
            upgrade()
            log_info("Migrations completed successfully!")
            
            return True
            
    except Exception as e:
        log_error(f"Failed to run migrations: {e}")
        return False

def main():
    """Основная функция"""
    log_info("Database Migration Script")
    log_info("=" * 30)
    
    # Ждем PostgreSQL
    if not wait_for_postgres():
        log_error("Failed to connect to PostgreSQL")
        sys.exit(1)
    
    # Применяем миграции
    if not run_migrations():
        log_error("Failed to run migrations")
        sys.exit(1)
    
    log_info("Database setup completed successfully!")
    sys.exit(0)

if __name__ == "__main__":
    main()
