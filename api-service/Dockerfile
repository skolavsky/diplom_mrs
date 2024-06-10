FROM python:3.12.3-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu --no-cache-dir --upgrade

COPY /app /app
COPY /alembic /alembic
COPY alembic.ini /alembic.ini

EXPOSE 8888

RUN apt-get update && \
    apt-get install -y --no-install-recommends openssl && \
    apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY /certs/cert.pem /etc/ssl/certs
COPY /certs/key.pem /etc/ssl/private

#run in compose file
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8888", "--reload"]
