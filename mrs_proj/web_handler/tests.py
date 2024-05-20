from datetime import datetime, timedelta

from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from .models import Article

LOGIN = 'web_handler:login'

class WebHandlerViewsTest(TestCase):
    """
    Класс для тестирования представлений (views) веб-приложения.
    """

    def setUp(self):
        # Создание тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Создание тестового клиента
        self.client = Client()

    def test_login_view_with_invalid_credentials(self):
        """
        Тестирование представления для входа в систему (login view) с некорректными учетными данными.
        """

        # Получение URL-пути для входа
        login_url = reverse('web_handler:login')

        # Проверка POST-запроса с некорректными учетными данными
        response = self.client.post(login_url,
                                    {'action': 'login', 'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Неправильные логин или пароль.')

        # Проверка, что пользователь не аутентифицирован
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class LoginViewTests(TestCase):
    '''
    Класс для тестирования логина
    '''

    def test_login_page_includes_js_code(self):
        '''
        Проверка на включение функции js кода на показ пароля
        :return:
        '''
        response = self.client.get(reverse('web_handler:login'))

        # Проверяем, что страница возвращает успешный статус
        self.assertEqual(response.status_code, 200)

        # Проверяем наличие вашего JavaScript-кода в ответе
        self.assertContains(response, 'show_hide_password(this)')

    def test_js_toggle_password(self):
        '''
        Проверка на страницу логина
        :return:
        '''
        response = self.client.get(reverse('web_handler:login'))
        # Проверяем, что страница возвращает успешный статус
        self.assertEqual(response.status_code, 200)

    def test_login_with_empty_password(self):
        '''
        Проверка на вход без пароля
        :return:
        '''
        response = self.client.post(reverse('web_handler:login'), {'username': 'testuser', 'password': ''})
        self.assertEqual(response.status_code, 400)

    def test_login_with_empty_login(self):
        '''
        Проверка на вход без логина
        :return:
        '''
        response = self.client.post(reverse('web_handler:login'), {'username': '', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 400)

    def test_login_with_empty_fields(self):
        '''
        Проверка на вход без заполнения полей
        :return:
        '''
        response = self.client.post(reverse('web_handler:login'), {'username': '', 'password': ''})
        self.assertEqual(response.status_code, 400)

    def test_failed_login(self):
        '''
        Тест на вход с неверными данными
        :return:
        '''
        response = self.client.post(reverse('web_handler:login'),
                                    {'username': 'invalid_user', 'password': 'invalid_password'})
        self.assertEqual(response.status_code, 400)

    def test_failed_login_button(self):
        '''
        Проверка на наличие кнопки с текстом "Войти" в ответе
        :return:
        '''
        response = self.client.get(reverse('web_handler:login'))
        self.assertContains(response, '<button type="submit">Войти</button>')

    def test_failed_login_header(self):
        '''
        Проверка наличия кнопки с текстом "ВХОД" и классом "button_open" в ответе
        :return:
        '''
        response = self.client.get(reverse('web_handler:login'))
        self.assertContains(response, '<h1>MRS</h1>')

    def test_login_title(self):
        '''
        Проверка соответствия заголовка страницы
        :return:
        '''
        response = self.client.get(reverse('web_handler:login'))
        self.assertContains(response, '<title>Вход</title>')

    def test_failed_login_password_wrong_type(self):
        '''
        Проверка на вход с неверным типом пароля
        :return:
        '''
        response = self.client.post(reverse('web_handler:login'), {'username': 'testuser', 'password': 123123})
        self.assertEqual(response.status_code, 400)

    def test_failed_login_password_wrong_symbols(self):
        '''
        Проверка на вход с неверным типом пароля(float)
        :return:
        '''
        response = self.client.post(reverse('web_handler:login'), {'username': 'testuser', 'password': 12312.123121})
        self.assertEqual(response.status_code, 400)
