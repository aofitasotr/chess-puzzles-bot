"""
Современный асинхронный загрузчик данных для шахматных головоломок
Использует COPY команду PostgreSQL для максимальной производительности
"""
import os
import time
import tempfile
from typing import Optional
import pandas as pd
import asyncio
import asyncpg
from dotenv import load_dotenv
from app.logger import log_info, log_warning, log_error

# Загружаем переменные окружения
load_dotenv()


async def load_puzzles_async(csv_path: str = 'app/db/data/lichess_db_puzzle.csv') -> int:
    """
    Асинхронная загрузка головоломок с использованием COPY команды
    Максимально быстрая загрузка данных
    """
    start_time = time.time()
    
    try:
        if not os.path.exists(csv_path):
            log_warning(f"CSV file {csv_path} not found, skipping...")
            return 0
        
        log_info(f"Starting load from {csv_path}...")
        
        # Читаем CSV с помощью pandas для быстрой обработки
        df = pd.read_csv(csv_path, usecols=['FEN', 'Moves', 'Rating', 'OpeningTags'])
        
        # Подготавливаем данные для COPY команды
        df = df.rename(columns={
            'FEN': 'fen',
            'Moves': 'moves', 
            'Rating': 'rating',
            'OpeningTags': 'tag'
        })
        
        # Обрабатываем пустые значения
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        df['tag'] = df['tag'].fillna('')
        
        # Получаем параметры подключения из переменных окружения
        conn_params = {
            'host': os.getenv('POSTGRES_HOST'),
            'port': int(os.getenv('POSTGRES_PORT')),
            'user': os.getenv('POSTGRES_USER'),
            'password': os.getenv('POSTGRES_PASSWORD'),
            'database': os.getenv('POSTGRES_DB')
        }
        
        # Загружаем данные с помощью COPY команды
        puzzles_loaded = await _copy_data_async(df, conn_params)
        
        elapsed_time = time.time() - start_time
        rate = puzzles_loaded / elapsed_time if elapsed_time > 0 else 0
        log_info(f"Successfully loaded {puzzles_loaded} puzzles in {elapsed_time:.2f}s ({rate:.0f} puzzles/sec)")
        
        return puzzles_loaded
        
    except Exception as e:
        log_error(f"Error loading CSV: {e}")
        raise


async def _copy_data_async(df: pd.DataFrame, conn_params: dict) -> int:
    """Асинхронная загрузка данных с использованием COPY команды"""
    try:
        # Создаем временный CSV файл для COPY команды
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8') as temp_file:
            # Записываем данные в формате, подходящем для COPY
            df.to_csv(temp_file, index=False, header=False, na_rep='')
            temp_file_path = temp_file.name
        
        try:
            # Подключаемся к PostgreSQL
            conn = await asyncpg.connect(**conn_params)
            
            try:
                # Выполняем COPY команду для максимальной скорости
                with open(temp_file_path, 'rb') as f:
                    result = await conn.copy_to_table(
                        'puzzle',
                        source=f,
                        columns=['fen', 'moves', 'rating', 'tag'],
                        format='csv'
                    )
                
                # Получаем количество загруженных записей
                count = await conn.fetchval("SELECT COUNT(*) FROM puzzle")
                
                return count
                
            finally:
                await conn.close()
                
        finally:
            # Удаляем временный файл
            os.unlink(temp_file_path)
            
    except Exception as e:
        log_error(f"Error in COPY operation: {e}")
        raise


def main() -> bool:
    """Основная функция для загрузки данных"""
    log_info("Data Loading Script")
    log_info("=" * 40)
    
    try:
        # Используем асинхронную загрузку с COPY командой
        log_info("Loading puzzles...")
        puzzles_loaded = asyncio.run(load_puzzles_async())
        
        if puzzles_loaded > 0:
            log_info(f"Data loading completed! Loaded {puzzles_loaded} puzzles.")
        else:
            log_warning("No puzzles were loaded.")
        
        return True
        
    except Exception as e:
        log_error(f"Failed to load data: {e}")
        return False


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)