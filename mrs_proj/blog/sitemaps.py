from django.contrib.sitemaps import Sitemap

from .models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated


class WebHandlerSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        # Возвращаем список URL-адресов из приложения web_handler
        return ['contacts', 'login', 'home']  # Список URL-адресов для вашего случая

    def location(self, item):
        # Возвращаем URL-адреса, соответствующие именам путей
        if item == 'contacts':
            return '/contacts/'
        elif item == 'login':
            return '/login/'
        elif item == 'home':
            return '/'
