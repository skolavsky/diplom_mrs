import time
from django.test import Client
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from django.urls import reverse


class WebHandlerTests(LiveServerTestCase):
    def setUp(self):
        # Создание экземпляра драйвера в методе setUp
        self.driver = webdriver.Chrome()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Создание тестового клиента
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_login_page(self):
        # Открываем страницу входа
        self.driver.get(self.live_server_url + '/login/')

        # Находим элементы формы входа
        username_input = self.driver.find_element(By.NAME, 'username')
        password_input = self.driver.find_element(By.NAME, 'password')
        submit_button = self.driver.find_element(By.XPATH, '//button[@type="submit"]')

        # Вводим данные в форму
        username_input.send_keys('testuser')
        password_input.send_keys('testpassword')

        # Отправляем форму
        submit_button.click()

        # Далее ваш код проверок

        # Ждем несколько секунд (может понадобиться подождать, пока страница загрузится)
        time.sleep(2)

        self.assertIn("/", self.driver.current_url)

    def test_home_page_contains_expected_content(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Главная страница')

        # Проверка наличия других ожидаемых элементов, например, вашего списка пациентов
        self.assertContains(response, 'Записи, без результатов')
        self.assertContains(response, 'YOUR SITE NAME')  # замените на фактическое имя вашего сайта

        # Проверка отсутствия ошибок в выводе
        self.assertNotContains(response, 'Error')

        # Пример проверки ссылок
        self.assertContains(response, f'href="{reverse("client_list")}"')
        self.assertContains(response, f'href="{reverse("contacts")}"')
        self.assertContains(response, f'href="{reverse("dashboard")}"')

    def tearDown(self):
        # Закрытие браузера после завершения теста
        self.driver.quit()
