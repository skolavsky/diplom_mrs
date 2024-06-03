import smtplib
from dotenv import load_dotenv
import os
import ssl
from dependencies import get_preferred_language
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


load_dotenv()

def make_mail(subject, body, sender, recipients: list):
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = ', '.join(recipients)
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    return message

def send_email(message, recipients):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host=os.getenv('SMTP_SERVER'),port=os.getenv('SMTP_PORT'), context=context) as server:
        server.login(os.getenv('SMTP_USERNAME'), os.getenv('SMTP_PASSWORD'))
        server.sendmail(os.getenv('SMTP_USERNAME'), recipients, message.as_string())

async def send_registration_email(locale: str, email: str):
    lang = get_preferred_language(locale)

    if lang == 'ru':
        subject = 'Добро пожаловать в api-сервис'
        body = 'Вы были зарегистрированы в api-service'
    else:
        subject = 'Welcome to api-service'
        body = 'You have been registered in api-service'
    try:
        message = make_mail(subject, body, os.getenv('SMTP_USERNAME'), [email])

        send_email(message, [email])
    except Exception as e:
        print(e)
        return False

    return True

async def send_changed_password_email(locale: str, email: str):
    lang = get_preferred_language(locale)

    if lang == 'ru':
        subject = 'Изменение пароля в api-сервисе'
        body = 'Ваш пароль был изменен в api-service'
    else:
        subject = 'Changed password in api-service'
        body = 'Your password has been changed in api-service'
    try:
        message = make_mail(subject, body, os.getenv('SMTP_USERNAME'), [email])

        send_email(message, [email])
    except Exception as e:
        print(e)
        return False

    return True

async def send_deleted_email(locale: str, email: str):
    lang = get_preferred_language(locale)

    if lang == 'ru':
        subject = 'Ваш аккаунт в api-сервисе был удален'
        body = 'Ваш аккаунт был удален в api-service'
    else:
        subject = 'Your account in api-service has been deleted'
        body = 'Your account has been deleted in api-service'
    try:
        message = make_mail(subject, body, os.getenv('SMTP_USERNAME'), [email])

        send_email(message, [email])
    except Exception as e:
        print(e)
        return False

    return True
