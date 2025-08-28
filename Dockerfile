#Используем образ Python 3.13.3
FROM python:3.13.3-slim

#Устанавливаем рабочую директорию в контейнере
WORKDIR /app

#Копируем файл зависимостей
COPY requirements.txt .

#Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь исходный код в контейнер
COPY . .

# Команда для запуска приложения
CMD ["python", "run.py"]