import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from decouple import config

dotenv_path = 'mrs_proj/mrs_proj/.env'
config.search_path = dotenv_path
BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')

TELEGRAM_API_BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'


def get_updates(offset=None):
    url = f'{TELEGRAM_API_BASE_URL}/getUpdates'
    params = {'offset': offset, 'timeout': 30}
    response = requests.get(url, params=params)
    return response.json()


def send_message(chat_id, text, reply_markup=None):
    url = f'{TELEGRAM_API_BASE_URL}/sendMessage'

    if reply_markup:
        data = {'chat_id': chat_id, 'text': text, 'reply_markup': reply_markup}
    else:
        data = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, json=data)
    return response.json()


def send_menu(chat_id):
    menu = {
        'keyboard': [['/start', '/help']],
        'resize_keyboard': True
    }
    send_message(chat_id, 'Выберите опцию:', reply_markup=menu)


def handle_message(chat_id, text):
    send_message(chat_id, 'Этот бот пока ничего не умеет. Но мы работаем над этим!')
    if text == '/start':
        send_menu(chat_id)
    elif text == '/help':
        send_message(chat_id, 'Этот бот пока ничего не умеет. Но мы работаем над этим!')
    else:
        send_message(chat_id, f'Я получил ваше сообщение: {text}')


def main():
    last_update_id = None
    while True:
        updates = get_updates(offset=last_update_id)
        if updates['ok']:
            for update in updates['result']:
                last_update_id = update['update_id'] + 1
                message = update.get('message')
                if message:
                    chat_id = message['chat']['id']
                    text = message.get('text')
                    handle_message(chat_id, text)


if __name__ == '__main__':
    main()
