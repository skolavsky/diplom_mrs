from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

LOGIN = '/login/'


class WebHandlerViewsTest(TestCase):
    """
    Класс для тестирования представлений (views) веб-приложения.
    """

    def setUp(self):
        # Создание тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Создание тестового клиента
        self.client = Client()

    def test_login_view(self):
        """
        Тестирование представления для входа в систему (login view).

        - Проверка GET-запроса к представлению входа в систему.
        - Проверка POST-запроса с корректными учетными данными.
        - Проверка POST-запроса с некорректными учетными данными.
        """

        # Проверка GET-запроса к представлению входа в систему
        response = self.client.get(LOGIN)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        # Проверка POST-запроса с корректными учетными данными
        response = self.client.post(LOGIN,
                                    {'action': 'login', 'username': 'testuser', 'password': 'testpassword'})
        self.assertRedirects(response, reverse('home'))  # Ожидается код перенаправления

    def test_login_view_with_invalid_credentials(self):
        """
        Тестирование представления для входа в систему (login view) с некорректными учетными данными.
        """

        # Проверка POST-запроса с некорректными учетными данными
        response = self.client.post(LOGIN,
                                    {'action': 'login', 'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Неправильные логин или пароль.')

    def test_contacts_view(self):
        """
        Тестирование представления контактов (contacts view).

        - Аутентификация пользователя.
        - Проверка GET-запроса к представлению контактов.
        """

        # Аутентификация пользователя
        self.client.login(username='testuser', password='testpassword')

        # Проверка GET-запроса к представлению контактов
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contacts.html')

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

    def test_dashboard_view(self):
        """
        Тестирование представления панели управления (dashboard view).

        - Аутентификация пользователя.
        - Проверка GET-запроса к представлению панели управления.
        """

        # Аутентификация пользователя
        self.client.login(username='testuser', password='testpassword')

        # Проверка GET-запроса к представлению панели управления
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_unauthenticated_access(self):
        """
        Тестирование доступа к представлениям без аутентификации.

        - Проверка доступа к представлению контактов без аутентификации.
        - Проверка доступа к представлению домашней страницы без аутентификации.
        - Проверка доступа к представлению панели управления без аутентификации.
        """

        # Проверка доступа к представлению контактов без аутентификации
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 302)  # Ожидается код перенаправления

        # Проверка доступа к представлению домашней страницы без аутентификации
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  # Ожидается код перенаправления

        # Проверка доступа к представлению панели управления без аутентификации
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)  # Ожидается код перенаправления

        # Проверка доступа к представлению домашней страницы без результатов пациентов
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  # Ожидается код перенаправления
        self.assertRedirects(response, '/login/?next=/', target_status_code=200)
        # Ожидается перенаправление на страницу входа с сохранением параметра 'next'