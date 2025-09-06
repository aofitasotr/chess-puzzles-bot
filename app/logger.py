import logging
import sys
from datetime import datetime
import os

class ColoredFormatter(logging.Formatter):
    """Цветной форматтер для логов"""
    
    # Цвета для разных уровней
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        # Добавляем цвет к уровню логирования
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.RESET}"
        
        # Добавляем эмодзи для разных уровней
        emoji_map = {
            'DEBUG': '🔍',
            'INFO': '✅',
            'WARNING': '⚠️',
            'ERROR': '❌',
            'CRITICAL': '💥'
        }
        
        emoji = emoji_map.get(record.levelname.replace(self.COLORS.get(record.levelname, ''), '').replace(self.RESET, ''), '📝')
        
        # Форматируем сообщение
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        formatted = f"{emoji} [{timestamp}] {record.levelname}: {record.getMessage()}"
        
        return formatted

def setup_logger(name='chess-puzzles-bot', level=logging.INFO):
    """Настраивает логгер для приложения (только консоль)"""
    
    # Создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Убираем существующие обработчики
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Создаем обработчик для консоли (stderr для Docker)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(level)
    
    # Применяем цветной форматтер
    formatter = ColoredFormatter()
    console_handler.setFormatter(formatter)
    
    # Добавляем обработчик к логгеру
    logger.addHandler(console_handler)
    
    # Включаем пропагацию для корневого логгера
    logger.propagate = True
    
    return logger

# Создаем глобальный логгер
logger = setup_logger()

# Функции для удобного использования
def log_info(message):
    """Логирует информационное сообщение"""
    logger.info(message)
    sys.stderr.flush()

def log_warning(message):
    """Логирует предупреждение"""
    logger.warning(message)
    sys.stderr.flush()

def log_error(message):
    """Логирует ошибку"""
    logger.error(message)
    sys.stderr.flush()

def log_debug(message):
    """Логирует отладочную информацию"""
    logger.debug(message)
    sys.stderr.flush()

def log_critical(message):
    """Логирует критическую ошибку"""
    logger.critical(message)
    sys.stderr.flush()
