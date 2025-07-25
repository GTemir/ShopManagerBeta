# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем переменные окружения для Flask
ENV FLASK_APP=app
ENV FLASK_ENV=development

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt
RUN apt update && apt install -y sqlite3
RUN mkdir -p /app/static/uploads
# Копируем исходный код
COPY . .

# Открываем порт 5000
EXPOSE 5000

# Запускаем приложение
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
