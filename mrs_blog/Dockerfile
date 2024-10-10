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

WORKDIR /app/


# Собираем статические файлы
RUN python manage.py collectstatic --noinput


# Выполняем миграции
RUN python manage.py makemigrations
RUN python manage.py migrate


# Команда для запуска Uvicorn
CMD ["uvicorn", "mrs_blog.asgi:application", "--host", "localhost", "--port", "8001"]
