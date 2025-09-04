from flask_sqlalchemy import SQLAlchemy
import time

db = SQLAlchemy()

def init_db(app):
    """Инициализация базы данных с повторными попытками"""
    max_retries = 3
    retry_delay = 3
    
    for attempt in range(max_retries):
        try:
            with app.app_context():
                db.create_all()
                print("✅ Database tables created successfully!")
                return
        except Exception as e:
            print(f"❌ Database connection attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                print(f"⏳ Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("💥 Failed to connect to database after all retries")
                raise

def get_db():
    """Получить экземпляр базы данных"""
    return db
