from flask import Blueprint
from app.database import db

# Создаем Blueprint для маршрутов
main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
    return "Hello, Flask in Docker!"
