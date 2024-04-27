from datetime import datetime, timedelta

from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from .models import Article

LOGIN = 'web_handler:login'


class DashboardViewTests(TestCase):
    def setUp(self):
        # Создаем пользователя для тестов
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Создаем несколько статей для пользователя
        self.article1 = Article.objects.create(
            title='Article 1',
            content='Content 1',
            author=self.user,
            created_at=datetime.now(),
            last_modified_at=datetime.now(),
        )
        self.article2 = Article.objects.create(
            title='Article 2',
            content='Content 2',
            author=self.user,
            created_at=datetime.now() - timedelta(days=1),
            last_modified_at=datetime.now() - timedelta(days=1),
        )

    def test_dashboard_view(self):
        # Авторизуем пользователя
        self.client.login(username='testuser', password='testpassword')

        # Запрашиваем страницу dashboard
        response = self.client.get(reverse('web_handler:dashboard'))

        # Проверяем, что ответ имеет код 200 (успешный запрос)
        self.assertEqual(response.status_code, 200)

        # Проверяем, что на странице отображаются данные из статей
        self.assertContains(response, 'Article 1')
        self.assertContains(response, 'Article 2')
        self.assertContains(response, 'Content 1')
        self.assertContains(response, 'Content 2')

    def test_dashboard_view_with_unauthenticated_user(self):
        # Выходим из системы пользователя
        self.client.logout()

        # Запрашиваем страницу dashboard
        response = self.client.get(reverse('web_handler:dashboard'))

        # Проверяем, что ответ имеет код 302 (редирект на страницу входа)
        self.assertEqual(response.status_code, 302)

        # Проверяем, что происходит редирект на страницу входа
        self.assertRedirects(response, '/login/?next=/dashboard/')

    def test_dashboard_view_with_no_articles(self):
        # Удаляем все статьи
        Article.objects.all().delete()

        # Авторизуем пользователя
        self.client.login(username='testuser', password='testpassword')

        # Запрашиваем страницу dashboard
        response = self.client.get(reverse('web_handler:dashboard'))

        # Проверяем, что ответ имеет код 200 (успешный запрос)
        self.assertEqual(response.status_code, 200)

        # Проверяем, что на странице отсутствуют данные статей
        self.assertNotContains(response, 'Article 1')
        self.assertNotContains(response, 'Article 2')
        self.assertNotContains(response, 'Content 1')
        self.assertNotContains(response, 'Content 2')


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

    def test_home_view(self):
        """
        Тестирование представления домашней страницы (home view).

        - Аутентификация пользователя.
        - Проверка GET-запроса к представлению домашней страницы.
        """

        # Аутентификация пользователя
        self.client.login(username='testuser', password='testpassword')

        # Проверка GET-запроса к представлению домашней страницы
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


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
        Проверка на наличие кнопки с текстом "ВХОД" и классом "button_open" в ответе
        :return:
        '''
        response = self.client.get(reverse('web_handler:login'))
        self.assertContains(response, '<button type="submit" class="button_open">ВХОД</button>')

    def test_failed_login_header(self):
        '''
        Проверка наличия кнопки с текстом "ВХОД" и классом "button_open" в ответе
        :return:
        '''
        response = self.client.get(reverse('web_handler:login'))
        self.assertContains(response, '<h1>ВХОД В СИСТЕМУ</h1>')

    def test_login_title(self):
        '''
        Проверка соответствия заголовка страницы
        :return:
        '''
        response = self.client.get(reverse('web_handler:login'))
        self.assertContains(response, '<title>Вход в систему</title>')

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
