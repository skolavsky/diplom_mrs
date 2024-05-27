# Dockerfile

# Базовый образ Python
FROM python:3.12

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

# Создание рабочего каталога
WORKDIR /app

# Копирование файлов приложения
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/

# Перейти на директорию выше для запуска Uvicorn

WORKDIR /app/mrs_proj

# Копируем скрипт ожидания
COPY wait_for_db.py /wait_for_db.py

# Собираем статические файлы
RUN python manage.py collectstatic --noinput


# Установка переменной окружения DJANGO_SETTINGS_MODULE
ENV DJANGO_SETTINGS_MODULE=mrs_proj.settings

# Выполняем миграции
RUN python manage.py makemigrations


# Команда для запуска Uvicorn
CMD ["uvicorn", "mrs_proj.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
