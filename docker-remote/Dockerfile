# Dockerfile.github

# Базовый образ Python
FROM python:3.12

# Установка зависимостей и git
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    git

# Создание рабочего каталога
WORKDIR /app

# Клонирование репозитория
ARG REPO_URL
ARG BRANCH=main
RUN git clone -b ${BRANCH} ${REPO_URL} .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

COPY .env /app/mrs_proj

WORKDIR /app/mrs_proj

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Установка переменной окружения DJANGO_SETTINGS_MODULE
ENV DJANGO_SETTINGS_MODULE=mrs_proj.settings


# Выполняем миграции
RUN python manage.py makemigrations
RUN python manage.py migrate

WORKDIR /app/mrs_proj


# Команда для запуска Uvicorn
CMD ["uvicorn", "mrs_proj.asgi:application", "--host", "0.0.0.0", "--port", "8000"]