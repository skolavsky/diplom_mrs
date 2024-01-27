# Используйте официальный образ Python с конкретной версией
FROM python:3.12

# Устанавливаем переменную окружения для запуска в неинтерактивном режиме
ENV DEBIAN_FRONTEND=noninteractive

# Устанавливаем git
RUN apt-get update && apt-get install -y git

# Создаем и переходим в рабочую директорию
WORKDIR /app

# Копируем файлы
COPY mrs_proj /app/mrs_proj/
COPY requirements.txt /app/

# Клонируем ваш репозиторий из GitHub
RUN git clone https://github.com/ElGansoDorado/Diplom

# Устанавливаем зависимости
RUN pip install -r /app/requirements.txt

# Устанавливаем Gunicorn
RUN pip install gunicorn

# Копируем файл конфигурации Gunicorn
COPY gunicorn.conf.py /app

# Копируем файлы, включая manage.py
COPY mrs_proj /app/mrs_proj/

# Устанавливаем переменную окружения с путем к статическим файлам
ENV DJANGO_SETTINGS_MODULE="mrs_proj.settings"

# Устанавливаем STATIC_ROOT
RUN python /app/mrs_proj/manage.py collectstatic --noinput

# Добавляем Nginx
RUN apt-get install -y nginx

# Копируем конфигурацию Nginx
COPY nginx.conf /etc/nginx/sites-available/default

# Открываем порт 80 для Nginx
EXPOSE 80

# Запускаем Gunicorn
CMD ["gunicorn", "--config", "/app/gunicorn.conf.py", "mrs_proj.wsgi:application"]

