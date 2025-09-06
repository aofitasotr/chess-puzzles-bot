FROM amancevice/pandas:2.3.2

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Создаем папку для логов
RUN mkdir -p /app/logs

# Копируем код приложения
COPY app/ app/
COPY run.py .

# Слушаем порт 5000
EXPOSE 5000

# Команда для запуска
CMD ["python", "run.py"]