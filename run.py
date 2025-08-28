import os
from flask import Flask
from dotenv import load_dotenv 

load_dotenv()  # загрузить переменные из .env

app = Flask(__name__)  #__name__ сообщает Flask, где находится приложение, чтобы правильно настроить пути к ресурсам


@app.route("/")  # def home() обрабатывает запросы по адресу "/" (корень сайта)
def home():
    return "Hello, Flask in Docker!"

if __name__ == "__main__":
    host = os.getenv("FLASK_HOST")
    port = int(os.getenv("FLASK_PORT"))
    app.run(host=host, port=port, debug=True) 
