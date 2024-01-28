# Используйте официальный образ Python с конкретной версией
FROM python:3.12

# Устанавливаем переменную окружения для запуска в неинтерактивном режиме
ENV DEBIAN_FRONTEND=noninteractive

# Устанавливаем git и nginx
RUN apt-get update && \
    apt-get install -y git nginx && \
    rm -rf /var/lib/apt/lists/*

# Создаем и переходим в рабочую директорию
WORKDIR /app

# Копируем файлы
COPY . /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Клонируем ваш репозиторий из GitHub (если это необходимо)

# Устанавливаем Gunicorn
RUN pip install gunicorn

# Копируем файл конфигурации Gunicorn
COPY gunicorn.conf.py /app

# Копируем конфигурацию Nginx
COPY nginx.conf /etc/nginx/sites-available/default

# Устанавливаем переменную окружения с путем к статическим файлам
ENV DJANGO_SETTINGS_MODULE="mrs_proj.settings"

# Устанавливаем STATIC_ROOT
RUN python mrs_proj/manage.py collectstatic --noinput

# Открываем порт 80 для Nginx
EXPOSE 80

# Запускаем Gunicorn
CMD ["gunicorn", "--config", "/app/gunicorn.conf.py", "mrs_proj.wsgi:application"]