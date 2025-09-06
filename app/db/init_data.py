#!/usr/bin/env python3
"""
Скрипт для инициализации данных - копирует CSV в volume и загружает данные
"""

import os
import sys
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Импортируем логгер
from app.logger import log_info, log_error, log_warning

def check_csv_exists():
    """Проверяет, существует ли CSV файл"""
    csv_path = 'app/db/data/lichess_db_puzzle.csv'
    
    if os.path.exists(csv_path):
        log_info("CSV file found")
        return True
    else:
        log_error(f"CSV file not found: {csv_path}")
        return False

def check_data_loaded():
    """Проверяет, загружены ли данные в базу"""
    try:
        from app import create_app
        from app.db.models import Puzzle
        
        app = create_app()
        with app.app_context():
            existing_puzzles = Puzzle.query.count()
            log_info(f"Found {existing_puzzles} puzzles in database")
            return existing_puzzles > 0
            
    except Exception as e:
        log_error(f"Failed to check data: {e}")
        return False

def load_data_if_needed():
    """Загружает данные только если их нет в базе"""
    if not check_data_loaded():
        log_info("No data found in database, loading from CSV...")
        
        # Импортируем функцию загрузки
        from app.db.data_loader import load_puzzles_async
        import asyncio
        
        # Загружаем из volume асинхронно
        puzzles_loaded = asyncio.run(load_puzzles_async('app/db/data/lichess_db_puzzle.csv'))
        log_info(f"Data loading completed! Loaded {puzzles_loaded} puzzles.")
    else:
        log_info("Data already loaded, skipping...")

def main():
    """Основная функция"""
    log_info("Data Initialization Script")
    log_info("=" * 35)
    
    try:
        # Проверяем наличие CSV файла
        if not check_csv_exists():
            log_error("CSV file not found")
            sys.exit(1)
        
        # Загружаем данные
        load_data_if_needed()
        
        log_info("Data initialization completed successfully!")
        sys.exit(0)
        
    except Exception as e:
        log_error(f"Failed to initialize data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
